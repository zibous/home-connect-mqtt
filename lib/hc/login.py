#!/usr/bin/env python3
# -*- coding':' utf-8 -*-

# -----------------------------------------------------------------------
# forced source from:
# https://github.com/osresearch/hcpy
#
# This directly follows the OAuth login flow that is opaquely described
# https://github.com/openid/AppAuth-Android
# A really nice walk through of how it works is:
# https://auth0.com/docs/get-started/authentication-and-authorization-flow/call-your-api-using-the-authorization-code-flow-with-pkce
#
# -----------------------------------------------------------------------

import os
import sys

_rootdir = os.path.dirname(os.path.realpath(__file__))
_hcdir = "{}/lib/hc".format(_rootdir)
_libdir = "{}/lib".format(_rootdir)

sys.path.append(_rootdir)
sys.path.append(_libdir)
sys.path.append(_hcdir)

try:
    import requests
    from urllib.parse import urlparse, parse_qs, urlencode
    from lxml import html
    import io
    import re
    import sys
    import json
    from time import time
    from base64 import b64decode as base64_decode
    from base64 import urlsafe_b64encode as base64url_encode
    from Crypto.Random import get_random_bytes
    from Crypto.Hash import SHA256
    from zipfile import ZipFile
    from xml2json import xml2json
except Exception as e:
    print('Import error {}, check requirements.txt'.format(e))

try:
    from lib import logger
    from lib import utils
    import config.app_config as app_config
except Exception as e:
    print('Application Configuration error {}, check settings.py'.format(e))
    sys.exit(1)


def b64(b):
    return re.sub(r'=', '', base64url_encode(b).decode('UTF-8'))

def b64random(num):
    return b64(base64url_encode(get_random_bytes(num)))

def getConfig(brand, connection) -> bool:
    """ get the devices config for the defined brand """

    log = logger.Log(__name__, app_config.LOGGER_LEVEL)

    try:

        log.info("hc login getConfig startet")

        _filename = "{}{}/{}".format(app_config.CONIG_DIR, brand, app_config.DEVICES_FILENAME)

        if os.path.isfile(_filename):
            log.info("config file {} present. Skip get config from cloud!".format(_filename))

            if "testcase" in connection:
                log.debug("Testcase enabled")
            else:
                return True
                
        _debugMode = False
        if app_config.APPS_MODE == "developer":            
            _debugMode = True

        # try to get the configuration from the bosch service
        log.info("Get Device configuration from Bosch Cloud")
        base_url = 'https://api.home-connect.com/security/oauth/'
        asset_url = 'https://prod.reu.rest.homeconnectegw.com/'

        # The app_id and scope are hardcoded in the application
        app_id = '9B75AC9EC512F36C84256AC47D813E2C1DD0D6520DF774B020E1E6E2EB29B1F3'
        scope = ["ReadAccount", "Settings", "IdentifyAppliance", "Control", "DeleteAppliance", "WriteAppliance", "ReadOrigApi", "Monitor", "WriteOrigApi", "Images"]

        verifier = b64(get_random_bytes(32))
        login_query = {
            "response_type": "code",
            "prompt": "login",
            "code_challenge": b64(SHA256.new(verifier.encode('UTF-8')).digest()),
            "code_challenge_method": "S256",
            "client_id": app_id,
            "scope": ' '.join(scope),
            "nonce": b64random(16),
            "state": b64random(16),
            "redirect_uri": 'hcauth://auth/prod',
            "redirect_target": 'icore',
        }

        loginpage_url = base_url + 'authorize?' + urlencode(login_query)
        auth_url = base_url + 'login'
        token_url = base_url + 'token'

        r = requests.get(loginpage_url)
        if r.status_code != requests.codes.ok:
            log.warning("error fetching login url: {}".format(loginpage_url))
            exit(1)

        loginpage = r.text

        tree = html.fromstring(loginpage)

        # add in the email and password
        auth_fields = {
            "email": connection["email"],
            "password": connection["password"],
            "code_challenge": login_query["code_challenge"],
            "code_challenge_method": login_query["code_challenge_method"],
            "redirect_uri": login_query["redirect_uri"],
        }

        for form in tree.forms:
            if form.attrib.get("id") != "login_form":
                continue
            for field in form.fields:
                if field not in auth_fields:
                    auth_fields[field] = form.fields.get(field)

        if _debugMode:
            log.debug("auth_fields: {}".format(auth_fields))

        # try to submit the form and get the redirect URL with the token
        r = requests.post(auth_url, data=auth_fields, allow_redirects=False)
        if r.status_code != 302:
            log.warning("Did not get a redirect; wrong username/password?: {}".format(r.text))
            exit(1)

        # Yes!
        location = r.headers["location"]
        url = urlparse(location)
        query = parse_qs(url.query)

        if _debugMode:
            log.debug("location: {}".format(location))
            log.debug("query: {}".format(query))

        code = query.get("code")
        if not code:
            log.warning("Unable to find code in response: {}".format(location))
            sys.exit(1)

        token_fields = {
            "grant_type": "authorization_code",
            "client_id": app_id,
            "code_verifier": verifier,
            "code": code[0],
            "redirect_uri": login_query["redirect_uri"],
        }

        if _debugMode:
            log.debug("token_fields: {}".format(token_fields))

        r = requests.post(token_url, data=token_fields, allow_redirects=False)
        if r.status_code != requests.codes.ok:
            log.warning("Bad code: {}, {}".format(r.headers, r.text))
            exit(1)

        token = json.loads(r.text)["access_token"]
        if _debugMode:
            log.debug("Received access token:{}".format(token))

        headers = {
            "Authorization": "Bearer " + token,
        }

        # now we can fetch the rest of the account info
        r = requests.get(asset_url + "account/details", headers=headers)
        if r.status_code != requests.codes.ok:
            log.warning("unable to fetch account details: {}, {}".format(r.headers, r.text))
            exit(1)

        if _debugMode:
            log.debug("Request Text: {}".format(r.text))

        account = json.loads(r.text)
        configs = []

        # save the accountdata if defined
        if _debugMode:
            _filename = "{}/{}/account.json".format(app_config.CONIG_DIR, brand)
            if utils.savefile(account, _filename):
                log.debug("Save account data to:{}".format(_filename))
            else:
                log.error("Save account data to:{}".format(_filename))

        for app in account["data"]["homeAppliances"]:

            app_brand = app["brand"]
            app_type = app["type"]
            app_id = app["identifier"]
            config = {
                "name": app_type.lower()
            }
            configs.append(config)

            if "tls" in app:
                # fancy machine with TLS support
                config["host"] = app_brand + "-" + app_type + "-" + app_id
                config["key"] = app["tls"]["key"]
                config["tls"] = True
                config["tlsmode"] = "fancy machine with TLS support"
            else:
                # less fancy machine with HTTP support
                config["host"] = app_id
                config["hostname"] = device["hostname"]
                config["key"] = app["aes"]["key"]
                config["iv"] = app["aes"]["iv"]
                config["tls"] = False
                config["tlsmode"] = "less fancy machine with HTTP support"

            config["friendly_name"] = app["name"]
            config["brand"] = app["brand"]
            config["type"] = app_type
            config["identifier"] = app_id

            if app_config.HA_DISCOVERY:
                config["brandname"] = brand.lower()
                config["deviceid"] = "{}-{}".format(brand, config["name"])
                config["discovery_prefix"] = app_config.HA_DISCOVERY_PREFIX
                config["ha_schema"] = "{}{}/{}/{}".format(app_config.CONIG_DIR, brand, config["name"], app_config.HA_DISCOVERY_SCHEMA)
                config["ha_items"] = "{}{}/{}/{}".format(app_config.CONIG_DIR, brand, config["name"], app_config.HA_DISCOVERY_DISCOVERY)

            # Fetch the XML zip file for this device
            app_url = asset_url + "api/iddf/v1/iddf/" + app_id
            log.info("fetching: {}".format(app_url))

            r = requests.get(app_url, headers=headers)
            if r.status_code != requests.codes.ok:
                log.warning("{}: unable to fetch machine description? {}".format(app_id))
                next

            # we now have a zip file with XML, let's unpack them
            z = ZipFile(io.BytesIO(r.content))
            features = z.open(app_id + "_FeatureMapping.xml").read()
            description = z.open(app_id + "_DeviceDescription.xml").read()

            # convert xml settings to json
            machine = xml2json(features, description)

            if _debugMode:                
                _filename = "{}{}/{}/machine.json".format(app_config.CONIG_DIR, brand, app_type.lower())
                if utils.savefile(machine, _filename):
                    log.debug("Save account data to:{}".format(_filename))
                else:
                    log.error("Save account data to:{}".format(_filename))

            config["description"] = machine["description"]
            config["features"] = machine["features"]
            # additional attributes#
            config["config"] = connection[app_id]
            config["appsversion"] = app_config.APPS_VERSION
            config["created"] = app_config.getTimestamp()

            # save the configuration
            _filename = "{}{}/{}".format(app_config.CONIG_DIR, brand, app_config.DEVICES_FILENAME)
            if utils.savefile(configs, _filename, "json"):
                log.info("Save new Config saved:{}".format(_filename))
                return True
            else:
                log.error("Save new Config not saved:{}".format(_filename))

    except BaseException as e:
        log.error(f"{__name__}: FATAL ERROR hclogin   - {str(e)}, line {sys.exc_info()[-1].tb_lineno}")
        return False
