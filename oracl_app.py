'''
    Basic module representing an application in the data service
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

class oracl_app(object):
    'An Oracl Application'
    def __init__(self, appid):
        '''
        Get details about an Application in the system
        :param appid:
        :return:
        '''
        self.appid = appid

    def __repr__(self):
        return "%s(appid = '%s')" % \
               (self.__class__.__name__,
                self.appid
                )
    @property
    def info(self):
        '''
        Look up the basic details about the Application
        :return:
        '''
        appid = self.appid
        appdir = os.path.join(datadir, appid)
        app_info_path = os.path.join(appdir, "appinfo")
        try:
            with open(app_info_path, "r") as f:
                app_info = json.loads(f.read())
            return app_info
        except IOError:
            return {"Error":"Application <" + appid + "> not found",
                    "appid": appid, "status":"not found", "timestamp":time()}


    @staticmethod
    def new(appid):
        '''
        Create a new Application
        :param appid:
        :return:
        '''
        appdir = os.path.join(datadir, appid)
        app_info_path = os.path.join(appdir, "appinfo")
        try:
            os.makedirs(appdir)
            with open(app_info_path, "w") as f:
                app_info = {"appid": appid, "status":"created", "timestamp":time()}
                f.write(json.dumps(app_info, indent=4))
            return app_info
        except OSError:
            return {"Error":"Application <" + appid + "> already exists",
                    "appid": appid, "status":"exists", "timestamp":time()}


    def delete(self):
        '''
        Delete an Application
        :return:
        '''
        appid = self.appid
        appdir = os.path.join(datadir, appid)
        # app_info_path = os.path.join(appdir, "appinfo")
        try:
            shutil.rmtree(appdir)
            return {"appid": appid, "status":"removed", "timestamp":time()}
        except OSError:
            return {"Error":"Application <" + appid + "> not found",
                    "appid": appid, "status":"not found", "timestamp":time()}
