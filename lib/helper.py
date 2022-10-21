#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

class dataClass(object):
    """dynamic data class"""
    def __init__(self, properties):
        self.properties = properties

    @property
    def toJson(self):
        return self.__dict__["properties"]

    @property
    def getPayload(self):
        if "properties" in self.__dict__ and "payload" in self.properties:
            return self.__dict__["properties"]["payload"]
        return None

    def __getattr__(self, name):
        try:
            if "properties" in self.__dict__ and name in self.properties:
                return self.properties[name] # Or call a function, etc
            return self.__dict__[name]
        except BaseException as e:
            return None

    def __setattr__(self, name, value):
        if "properties" in self.__dict__ and name in self.properties:
            self.properties[name] = value
        else:
            self.__dict__[name] = value

class AttributeDict(object):
    """
    A class to convert a nested Dictionary into an object with key-values
    accessibly using attribute notation (AttributeDict.attribute) instead of
    key notation (Dict["key"]). This class recursively sets Dicts to objects,
    allowing you to recurse down nested dicts (like: AttributeDict.attr.attr)
    y = yaml.load(open(yaml_config_file, 'r'))
    myobj = AttributeDict(**y)
    """
    def __init__(self, **entries):
        self.add_entries(**entries)

    def add_entries(self, **entries):
        for key, value in entries.items():
            if type(value) is dict:
                self.__dict__[key] = AttributeDict(**value)
            else:
                self.__dict__[key] = value

    def __getitem__(self, key):
        """
        Provides dict-style access to attributes
        """
        return getattr(self, key)

class jsonobj(object):
    """ converts json object (Nested) to python object"""

    def __init__(self, data=None):
        for key, val in data.items():
            setattr(self, key, self.compute_attr_value(val))

    def compute_attr_value(self, value):
        if type(value) is list:
            return [self.compute_attr_value(x) for x in value]
        elif type(value) is dict:
            return jsonobj(value)
        else:
            return value

class dataObj(object):
    """dynmic data object"""
    pass
    @property
    def toJson(self):
        """all attributes to json"""
        return self.__dict__

def dumps(o) -> str:
    """helper method to convert dictionary to object"""
    try:
        return json.dumps(o, sort_keys=True, indent=4)
    except BaseException as e:
        print(f"Error {sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return ""

class prop(object):
    """porperty object"""
    def __init__(self, get_func):
        self.get_func = get_func
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.get_func(instance)
