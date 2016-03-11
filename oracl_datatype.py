'''
    Basic module representing an Application Data Type
'''
__author__ = 'hpreston'


import os, json, shutil
from time import time
# from uuid import uuid4

# The data directory should be set as an environment variable, if not set to default
if "oracl_datadir" in os.environ:
    datadir = os.environ["oracl_datadir"]
else:
    datadir = "data"

class oracl_datatype(object):
    'An Oracl Application'
    def __init__(self, appid, datatype):
        '''
        Create a new Application Data Type Object
        :param appid:
        :param datatype:
        :return:
        '''
        self.appid = appid
        self.datatype = datatype

    def __repr__(self):
        return "%s(appid = '%s', datatype = '%s')" % \
               (self.__class__.__name__,
                self.appid,
                self.datatype
                )
    @property
    def info(self):
        '''
        Look up the basic details about the Application Data Type
        :return:
        '''
        appid = self.appid
        datatype = self.datatype
        appdir = os.path.join(datadir, appid)
        datatypedir = os.path.join(appdir,datatype)
        datatype_info_path = os.path.join(datatypedir, "datatypeinfo")
        try:
            with open(datatype_info_path, "r") as f:
                datatype_info = json.loads(f.read())
            return datatype_info
        except IOError:
            return {"Error":"Data Type <" + datatype + "> in Application <" + appid + "> not found",
                    "appid": appid, "datatype":datatype, "status":"not found", "timestamp":time()}


    @staticmethod
    def new(appid, datatype):
        '''
        Create a new Data Type in an Application
        '''
        appdir = os.path.join(datadir, appid)
        datatypedir = os.path.join(appdir,datatype)
        datatype_info_path = os.path.join(datatypedir, "datatypeinfo")
        try:
            os.makedirs(datatypedir)
            with open(datatype_info_path, "w") as f:
                datatype_info = {"appid": appid, "datatype":datatype, "status":"created", "timestamp":time()}
                f.write(json.dumps(datatype_info, indent=4))
            return datatype_info
        except OSError:
            return {"Error":"Data Type <" + datatype + "> in Application <" + appid + "> already exists",
                    "appid": appid, "datatype":datatype, "status":"exists", "timestamp":time()}


    def delete(self):
        '''
        Delete an Application Data Type
        :return:
        '''
        appid = self.appid
        datatype = self.datatype
        appdir = os.path.join(datadir, appid)
        datatypedir = os.path.join(appdir,datatype)
        try:
            shutil.rmtree(datatypedir)
            return {"appid": appid, "datatype":datatype, "status":"removed", "timestamp":time()}
        except OSError:
            return {"Error":"Data Type <" + datatype + "> in Application <" + appid + "> not found",
                    "appid": appid, "datatype":datatype, "status":"not found", "timestamp":time()}
