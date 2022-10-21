#!/usr/bin/python3
# -*- coding":" utf-8 -*-
import sys
import os
from os import path
import glob
import imp

def getDeviceList(devicedir:str = "devices") ->dict:
   result = set()
   for path in glob.glob(f'{devicedir}/*/**/', recursive=True):       
       module_name= os.path.basename(os.path.dirname(path)) 
       if module_name == "__pycache__":
          continue
       if(os.path.isfile("{}/client.py".format(path))):  
          print(module_name)  
          result.add(module_name)
   return result

def findModule(name:str):   
   try:
      fp, path, desc = imp.find_module(name)
      print ("module found: {}, {},{}".format(name,path, desc))
   except ImportError:
        print ("module not found: " + name)

    