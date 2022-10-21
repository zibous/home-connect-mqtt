#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date, datetime
import sys
import os
import re
import json
import math
import string
import requests
import yaml
import csv
from argparse import Namespace
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from requests.exceptions import Timeout
from uptime import uptime


def is_port_in_use(server:str="localhost", port: int=80) -> bool:
    """checks if the port is allready used"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((server, port)) == 0

def encode_config_topic(string):
    """Encode a config topic to UTF-8."""
    return string.encode("ascii", "ignore").decode("utf-8")

def format_mac(mac):
    """Format the mac address string."""
    return ":".join(mac[i : i + 2] for i in range(0, 12, 2))

def get_first_of_month(date, month_offset=0):
    """get the first day of month
       zero based indexing of month to make math work
    """
    month_count = date.month - 1 + month_offset
    return date.replace(
        day=1, month=month_count % 12 + 1, year=date.year + (month_count // 12)
    )

def timestamp():
    return datetime.now().strftime('%Y/%m/%dT%H:%M:%S')

class read_data(object):
    def __init__(self, jdata):
        self.__dict__ = json.loads(jdata)


def loadYaml(filename: str = "") -> dict:
    if filename:
        with open(filename, 'r', encoding='utf8') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as exc:
                print(exc)
                return None

def make_recur_path(filename): 
    custom_path = os.path.dirname(filename)
    try: 
        os.makedirs(custom_path, exist_ok=True) 
        return True 
    except OSError: 
        return False 

def isFile(filename):
    try:
        if filename:
           return os.path.isfile(_filename)
    except BaseException as e:
        print(f"Error {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
    return False        

def write_to_file(data: str, filepath: str) -> bool:
    """appends the content(str) to the defined file"""
    try:
        _path = os.path.dirname(filepath)
        os.makedirs(_path, exist_ok=True) 
        with open(filepath, "w+", encoding='utf8') as f:
            f.write(data)
    except:
        raise Exception(f"Saving data to {filepath} encountered an error")

def saveDictToCsv(dict_data:dict=None, filename:str=None) -> bool:
    """saves a simple dict as csv content to the defined file"""
    try:
        if dict_data and filename:
            _path = os.path.dirname(filename)
            os.makedirs(_path, exist_ok=True) 
            addHeader = not os.path.isfile(filename)
            csv_file=open(filename,'a+', encoding='utf8')
            write=csv.writer(csv_file)
            if addHeader:
                    write.writerow(dict_data.keys())
            write.writerow(dict_data.values())
            csv_file.close()
            return True
    except BaseException as e:
        print(f"Error {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")

    return False

def savefile(content: any = "", filename: str = None, datatype: str = 'json') -> bool:
    """save the content to the defined file based on the datatype"""
    if not content:
        return False
    if filename and datatype:
        try:
            _path = os.path.dirname(filename)
            os.makedirs(_path, exist_ok=True) 
            if make_recur_path(filename):
                with open(filename, 'w', encoding='utf8') as f:
                    if datatype == 'json':
                        f.write(json.dumps(content, sort_keys=False, indent=4, ensure_ascii=False))
                    if datatype == 'text':
                        f.write(content)
                return True
        except BaseException as e:
            return False
    return False

def represent_str(dumper, instance):
    """representer for yaml file formatting"""
    if "\n" in instance:
        instance = re.sub(' +\n| +$', '\n', instance)
        return dumper.represent_scalar('tag:yaml.org,2002:str',instance,style='|')
    else:
        return dumper.represent_scalar('tag:yaml.org,2002:str',instance)

def saveDictAsYamlFile(data:dict=None, filename:str=None)->bool:
    """saved the dict data as yaml to the defined file"""
    try:
        _path = os.path.dirname(filename)
        os.makedirs(_path, exist_ok=True) 
        yaml.add_representer(str, represent_str)
        with open(filename, "w") as output:
            yaml.dump(data,
                    output,
                    allow_unicode=True,
                    encoding='utf-8',
                    default_flow_style=False)
    except BaseException as e:
        print(f"Error {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return False

    return True

def loadjsondata(filename: str = None, fallback: str = "") -> dict:
    """load the json data from the defined file"""
    try:
        if filename:
            if fallback != "":
                if not os.path.isfile(filename):
                    filename = filename.replace(".json", fallback)
            if os.path.isfile(filename):
                with open(filename, "r", encoding='utf8') as f:
                    data = json.load(f)
            return data
    except BaseException as e:
        print(f"Error {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return None

def getResponse(url: str = "", timeout: int = 5):
    """ get the http adapter response"""
    try:
        retry_strategy = Retry(total=3, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["HEAD", "GET", "OPTIONS"])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response
    except BaseException as e:
        print(f"Error {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return None

def getESBHomeData(url: str = "", platform: str = "sensor", id: str = "", timeout: int = 5) -> dict:
    """get the data from the defined platform and device id"""
    strURL = "{}/{}/{}".format(url, platform, id)
    # default data
    dictData = {
        "url": strURL,
        "field": id,
        "value": -1,
        "state": "loading",
        "responsecode": 400,
        "responsemessage": "not found!",
        "encoding": "none"
    }
    response = getResponse(url=strURL)
    if(response.status_code == 200):
        data = json.loads(response.text)
        if(data):
            dictData["field"] = data["id"]
            dictData["value"] = data["value"]
            dictData["state"] = "Ready"
            dictData["responsecode"] = response.status_code
            dictData["responsemessage"] = response.status_code
        else:
            dictData["state"] = "Error"
            dictData["responsecode"] = response.status_code
    return dictData


def format_duration(seconds, fmtlong:bool=False)->str:
    """format seconds to human readable format"""
    try:
        if seconds<1.00:
           return "{} ms".format(seconds*1000)
        if fmtlong:
            return runningTime(seconds)
        times = [("y", 365 * 24 * 60 * 60),
                 ("d", 24 * 60 * 60),
                 ("h", 60 * 60),
                 ("m", 60),
                 ("s", 1)]
        chunks = []
        for name, secs in times:
            qty = seconds // secs
            if qty:
                chunks.append(str(qty) + name)
            seconds = seconds % secs
        return ' '.join(chunks[:-1]) + ' ' + chunks[-1] if len(chunks) > 1 else chunks[0]
    except BaseException as e:
        print(f"Error {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return ""


def runningTime(total_seconds) -> str:
    """calculates the running time in days, hour, minute and seconds"""
    try:
        if total_seconds<1.00:
           return "{} ms".format(total_seconds*1000)
        MINUTE = 60
        HOUR = MINUTE * 60
        DAY = HOUR * 24
        # Get the days, hours, etc:
        days = int(total_seconds / DAY)
        hours = int((total_seconds % DAY) / HOUR)
        minutes = int((total_seconds % HOUR) / MINUTE)
        seconds = int(total_seconds % MINUTE)
        # Build up the pretty output (like this: "N days, N hours, N minutes, N seconds")
        output = ""
        if days > 0:
            output += str(days) + " " + (days == 1 and "day" or "days") + ", "
        if len(output) > 0 or hours > 0:
            output += str(hours) + " " + (hours == 1 and "hour" or "hours") + ", "
        if len(output) > 0 or minutes > 0:
            output += str(minutes) + " " + (minutes == 1 and "minute" or "minutes") + ", "
        output += str(seconds) + " " + (seconds == 1 and "second" or "seconds")
        return output
    except BaseException as e:
        print(f"Error {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return ""

def calcTimeElapsed(start:datetime=datetime.min, end:datetime=datetime.min) -> str:
        """get the elapsed time between end and start data"""
        diff = end - start
        if diff == 0: return "0 ms"
        return format_duration( diff.total_seconds() )

def repeat_string(a_string, target_length):
    """a_string * n with n as an integer to repeat a_string n number of times."""
    number_of_repeats = target_length // len(a_string) + 1
    a_string_repeated = a_string * number_of_repeats
    a_string_repeated_to_target = a_string_repeated[:target_length]
    return a_string_repeated_to_target

def up_time() -> str:
    """calculates the uptime"""
    total_seconds = uptime()
    return (runningTime(total_seconds))

def now():
    return datetime.now()

def strToDate(theDate, date_format:str="%Y-%m-%dT%H:%M:%S") -> datetime:
    """converts a string to a date object based on the format pattern"""
    try:
        if isinstance(theDate, str):
            return datetime.strptime(theDate, date_format)
        if isinstance(theDate, datetime):
            return theDate
    except BaseException as e:
        print(f"Error  {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return None

def dateToString(date_time, date_format:str="%Y-%m-%dT%H:%M:%S") -> str:
    """converts a date object to string based on the format pattern"""
    try:
        if isinstance(date_time, str):
            return date_time
        if isinstance(date_time, datetime):
            return date_time.strftime(date_format)
    except BaseException as e:
        print(f"Error {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return ""


def calcElapsedTime(start: str = "", end: str = None, date_format: str = "%Y-%m-%dT%H:%M:%S") -> int:
    """calculate the elpased time"""
    try:
        if end == None:
            end = datetime.now().strftime(date_format)
            diff = datetime.strptime(end, date_format) - datetime.strptime(start, date_format)
            return int(diff.total_seconds()/60)
    except BaseException as e:
        print(f"Error {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return 0


def hasDateTimeChanged(datestring: str = "", date_format: str = "%H", checkInitDate: bool = False) -> bool:
    """checks if the datastring to current timestamp has changed"""
    try:
        if checkInitDate and datestring == "0001-01-01 00:00:00":
            return False
        new = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S')
        return(new.strftime(date_format) != datetime.now().strftime(date_format))
    except BaseException as e:
        print(f"Error {__name__}:{sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
        return False

def round_digits(x: float = 0.00, decimal_places: int = 2) -> float:
    """helper to round a number based on the decimal places"""
    return round(x, decimal_places)


def round_3digits(x: float = 0.00) -> float:
    """helper to round a number to 3 digits"""
    return round(x, 3)

def isValidNumber(value)->bool:
    """checks if the value is a valid number"""
    return math.isfinite(value)

def addNumber(field1: float = 0.00, field2: float = 0.00) -> float:
    """helper to add to numbers"""
    result = round(float(field1) + float(field2), 3)
    return float(result)


def substructNumber(field1: float = 0.00, field2: float = 0.00) -> float:
    """helper to substract a number"""
    result = round(float(field1) - float(field2), 3)
    return float(result)


def divideNumber(field1: float = 0.00, field2: float = 0.00) -> float:
    """helper to get the result for divide"""
    if field2 > 0.00:
        result = round(float(field1) / float(field2), 3)
        return float(result)
    return 0.00


def calcTotal(field1: float = 0.00, field2: float = 0.00, field3: float = 0.00) -> float:
    """calcs the total for the defined fields"""
    result = round(float(field1) + float(field2) - float(field3), 3)
    return float(result)


def fix_float(value: float) -> float:
    """Fix precision for single-precision floats and return what was probably
    meant as a float.
    Unfortunately the float representation of 0.1 converted to a double is not the
    double representation of 0.1, but 0.10000000149011612.
    This methods tries to round to the closest decimal value that a float of this
    magnitude can accurately represent.
    """
    if value == 0 or not math.isfinite(value):
        return value
    abs_val = abs(value)
    # assume ~7 decimals of precision for floats to be safe
    l10 = math.ceil(math.log10(abs_val))
    prec = 7 - l10
    return round(value, prec)


def remove_umlaut(string) -> str:
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()
    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')
    string = string.decode('utf-8')
    return string


def generate_csv_data(data: dict) -> str:
    """generates the csv data form the defined dict items"""
    # Defining CSV columns in a list to maintain
    # the order
    csv_columns = data.keys()
    # Generate the first row of CSV
    csv_data = ",".join(csv_columns) + "\n"
    # Generate the single record present
    new_row = list()
    for col in csv_columns:
        new_row.append(str(data[col]))
    # Concatenate the record with the column information
    # in CSV format
    csv_data += ",".join(new_row) + "\n"
    return csv_data


def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    values = extract(obj, arr, key)
    return values


def flatten_json(nested_json) -> string:
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(nested_json)
    return out
