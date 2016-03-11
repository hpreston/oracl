'''
    Basic module representing an Application Data Type Data Element
'''
__author__ = 'hpreston'

# Todo - Add support for accessing data elements

import os, json, shutil
from time import time
# from uuid import uuid4

# The data directory should be set as an environment variable, if not set to default
if "oracl_datadir" in os.environ:
    datadir = os.environ["oracl_datadir"]
else:
    datadir = "data"

class oracl_element(object):
    'An Oracl Data Object for some Application Data Type'
    def __init__(self, appid, datatype, element):
        '''
        Create a new Data Element Object for an Application Data Type
        :param appid:
        :param datatype:
        :param element:
        :return:
        '''
        self.appid = appid
        self.datatype = datatype
        self.element = element

    def __repr__(self):
        return "%s(appid = '%s', datatype = '%s', element = '%s')" % \
               (self.__class__.__name__,
                self.appid,
                self.datatype,
                self.element
                )

    @property
    def info(self):
        '''
        Look up the basic details about the Data Element
        :return:
        '''
        appid = self.appid
        datatype = self.datatype
        element = self.element
        appdir = os.path.join(datadir, appid)
        datatypedir = os.path.join(appdir,datatype)
        element_path = os.path.join(datatypedir, element)
        try:
            with open(element_path, "r") as f:
                element_info = json.loads(f.read())["element_info"]
            return element_info
        except IOError:
            return {"Error":"Element <" + element + "> of Data Type <" + datatype + "> in Application <" + appid + "> not found",
                    "appid": appid, "datatype":datatype, "element":element, "status":"not found", "timestamp":time()}

    @property
    def element_data(self):
        '''
        Return the Data store in the Element
        :return:
        '''
        appid = self.appid
        datatype = self.datatype
        element = self.element
        appdir = os.path.join(datadir, appid)
        datatypedir = os.path.join(appdir,datatype)
        element_path = os.path.join(datatypedir, element)
        try:
            with open(element_path, "r") as f:
                element_info = json.loads(f.read())["element_data"]
            return element_info
        except IOError:
            return {"Error":"Element <" + element + "> of Data Type <" + datatype + "> in Application <" + appid + "> not found",
                    "appid": appid, "datatype":datatype, "element":element, "status":"not found", "timestamp":time()}

    @staticmethod
    def new(appid, datatype, element, data = {}):
        '''
        Create a new Element of a Data Type in an Application
        '''
        appdir = os.path.join(datadir, appid)
        datatypedir = os.path.join(appdir,datatype)
        element_path = os.path.join(datatypedir, element)
        if os.path.isfile(element_path):
            return {"Error":"Element <" + element + "> of Data Type <" + datatype + "> in Application <" + appid + "> already exists",
                    "appid": appid, "datatype":datatype, "element":element, "status":"exists", "timestamp":time()}
        try:
            with open(element_path, "w") as f:
                element_data = {"element_info":
                                    {"appid": appid,
                                     "datatype":datatype,
                                     "element":element,
                                     "status":"created",
                                     "timestamp":time()
                                     },
                                 "element_data":data
                                }
                f.write(json.dumps(element_data, indent=4))
            return element_data
        except OSError:
            return {"Error":"Element <" + element + "> of Data Type <" + datatype + "> in Application <" + appid + "> already exists",
                    "appid": appid, "datatype":datatype, "element":element, "status":"exists", "timestamp":time()}

    def delete(self):
        '''
        Delete an Element from an Application
        :return:
        '''
        appid = self.appid
        datatype = self.datatype
        element = self.element
        appdir = os.path.join(datadir, appid)
        datatypedir = os.path.join(appdir,datatype)
        element_path = os.path.join(datatypedir, element)
        print element_path
        try:
            os.remove(element_path)
            return {"appid": appid, "datatype":datatype, "element":element, "status":"removed", "timestamp":time()}
        except OSError:
            return {"Error":"Element <" + element + "> of Data Type <" + datatype + "> in Application <" + appid + "> not found",
                    "appid": appid, "datatype":datatype, "element":element, "status":"not found", "timestamp":time()}

