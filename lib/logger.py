#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import sys
import traceback
from time import gmtime, strftime


# class StructuredMessage(object):
#     """helper method structured message:
#        @call: logging.info(_('message 1', foo='bar', bar='baz', num=123, fnum=123.456))
#     """
#     def __init__(self, message, **kwargs):
#         self.message = message
#         self.kwargs = kwargs
#     def __str__(self):
#         return '%s >>> %s' % (self.message, json.dumps(self.kwargs))

# _ = StructuredMessage   # optional, to improve readability


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    light_blue = "\x1b[1;36m"
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    green = "\x1b[1;32m"
    magenta = "\x1b[1;35m"

    reset = '\x1b[0m'

    def __init__(self, fmt):
        """constructor for logger"""
        #super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.magenta + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        """message formatter"""
        log_fmt = self.FORMATS.get(record.levelno)
        date_fmt = "%Y/%m/%d %H:%M:%S"
        formatter = logging.Formatter(log_fmt, date_fmt)
        formatter.default_msec_format = '%s.%03d'
        return formatter.format(record)


class Log(object):
    """Logging wrapper for better output """

    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOLOG = 100

    LOGLEVELMAP = {
        "DEVELOP": logging.DEBUG,
        "PRODUCTION":logging.INFO,
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "NONE": 100,
        "NOLOG": 100
    }

    def __init__(self, name: str = 'applogger', level: int = 100, logDir: str = None, showLine: bool = False):
        """Constructor application logger
        Args:
            name (str, optional): [description]. Defaults to 'applogger'.
            level (int, optional): [description]. Defaults to logging.DEBUG.
            enableLogFile (bool, optional): [description]. Defaults to False
        """
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.settings(level=level, logDir=logDir,showLine=showLine)
        # self.logger.setLevel(level)
        # self.loglevel = level
        # self.logDir = logDir
        # if(logDir):
        #     # use log file
        #     fh = logging.FileHandler(self.logDir + '%s.log' % name, 'w')
        #     self.logger.addHandler(fh)
        # if(showLine):
        #     fmt = "%(asctime)s.%(msecs)03d  - %(levelname)s: %(message)s (%(name)s: Line %(lineno)d)"
        # else:
        #     fmt = "%(asctime)s.%(msecs)03d  - %(levelname)s: %(message)s"
        # sh = logging.StreamHandler()
        # sh.setFormatter(CustomFormatter(fmt))
        # self.logger.addHandler(sh)
        # sys.excepthook = self.handle_excepthook

    def settings(self, level: int = 100, logDir: str = None, showLine: bool = False):
        """setting for the logger"""
        self.logger.setLevel(level)
        self.loglevel = level
        self.logDir = logDir
        if(logDir):
            # use log file
            fh = logging.FileHandler(self.logDir + '%s.log' % self.name, 'w')
            self.logger.addHandler(fh)
        if(showLine):
            fmt = "%(asctime)s.%(msecs)03d  - %(levelname)s: %(message)s (%(name)s: Line %(lineno)d)"
        else:
            fmt = "%(asctime)s.%(msecs)03d  - %(levelname)s: %(message)s"
        sh = logging.StreamHandler()
        sh.setFormatter(CustomFormatter(fmt))
        self.logger.addHandler(sh)
        sys.excepthook = self.handle_excepthook    
    
    def setLoglevel(self, level: int = 100):
        self.logger.setLevel(level)
        self.loglevel = level

    def debug(self, msg):
        """log debug message"""
        self.logger.debug(msg)

    def info(self, msg):
        """log info message"""
        self.logger.info(msg)

    def warning(self, msg):
        """log warning message"""
        self.logger.warning(msg)

    def error(self, msg):
        """log error message"""
        self.logger.error(msg)

    def critical(self, msg):
        """log critical message"""
        self.logger.critical(msg)

    def print(self, msg: str = ' ', end: str = '\r'):
        """print helper method"""
        if(self.loglevel < 100):
            print(msg, end)
    def newLine(self, len:int=80):
        print("-" * len,'\r')
    def handle_excepthook_debug(self, type, message, stack):
        """"debug excepthook handle """
        self.logger.critical(f'An unhandled exception occured: {message}. Traceback: {traceback.format_tb(stack)}')

    def handle_excepthook(self, type, message, stack):
        """" excepthook handle """
        self.logger.error(f'An unhandled exception occured: {message}. Traceback: {traceback.extract_tb(stack,1)}')
