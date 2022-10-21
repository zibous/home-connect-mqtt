#!/usr/bin/python3
# -*- coding":" utf-8 -*-

from influxdb import InfluxDBClient
from datetime import datetime


class InfuxdbCient:

    version = "1.0.1"

    def __init__(self, database: str , host: str , port: int , user: str, passwd: str):
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.measurement = "data"
        self.errormessage = None
        self.fields = None
        self.time = datetime.utcnow().strftime(DATEFORMAT_UTC)
        self.influxClient = None
        self.__connect__()

    def __connect__(self):
        try:            
            self.influxClient = InfluxDBClient(
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.passwd
            )
            return True
        except BaseException as e:
            self.errormessage = f"{__name__} Error = {str(e)}"
            return False

    def post(self, fields, measurement: str = 'data', time: str = None):
        try:
            if self.influxClient:
                self.measurement = measurement
                self.fields = fields
                if time:
                    self.time = time
                if self.measurement and self.fields:                    
                    self.influxClient.write_points([{
                        "measurement": self.measurement,
                        "time": self.time,
                        "fields": self.fields
                    }], database=self.database)
        except BaseException as e:
            self.errormessage = f"{__name__} Error = {str(e)}"
            return False

    def get(self, query: str = None):
        try:
            if self.influxClient and query:                
                return self.influxClient.query(query)
        except BaseException as e:
            self.errormessage = f"{__name__} Error = {str(e)}"            
            return None
