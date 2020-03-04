# -*- coding: utf-8 -*-
import sys
import sys
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")
import os
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
import time
import datetime
from pymongo import MongoClient
from log.logger_pyflask import logging_instance
'''
    신한아이 인디 자동로그인 예제
'''

class autoLogin(QMainWindow):
    def __init__(self):
        self.processID = os.getpid()

        loginLogger = logging_instance("autoLogin.py   PID   "+(str)(self.processID)).mylogger

        super().__init__()
        self.flag= False
        start = time.time()
        client = MongoClient('127.0.0.1', 27017)
        db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
        db = client[db_name]
        collection = db["login_check"]
        collection_status_param = {
            "status": "Processing"
        }
        if collection.find():
            collection.insert(collection_status_param)
        else:
            for i in collection.find():
                try:
                    if i["status"] != "":
                        collection.update({
                            "status": i["status"]
                        }, {
                            "status": "Processing"
                        })
                        break
                    else:
                        collection.insert(collection_status_param)
                except Exception:
                    print(Exception)
                    QCoreApplication.exit(0)
        try:
            # 일반 TR OCX
            self.Indi_login = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
            loginLogger.info("OCX call")
            # 신한i Indi 자동로그인
            while True:
                if time.time() - start >=100:
                    break
                loginLogger.info("Login Trying" )
                login = self.Indi_login.StartIndi('xamevh123', 'florida1!23', 'florida1!23', 'C:\SHINHAN-i\indi\giexpertstarter.exe')
                print(login)
                if login == True :
                    self.flag = True
                    loginLogger.info("Login Success")
                    collection.update({
                        "status": "Processing"
                    }, {
                        "status": "Success"
                    })
                    break
            #QCoreApplication.exit(0)
        except Exception:
            loginLogger.info("Login Failure Exception occur")
            print(Exception)
            # QCoreApplication.exit(0)
        # QCoreApplication.exit(0)


class autoLoginCheck():
    def __init__(self):
        self.flag= False
        client = MongoClient('127.0.0.1', 27017)
        db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
        db = client[db_name]
        collection = db["login_check"]

        for i in collection.find():
            if i['status']== "Success":
                self.flag= True
            else:
                self.flag = False



if __name__ == "__main__":
    app = QApplication(sys.argv)
    IndiWindow = autoLogin()
    print("test")
    print(IndiWindow.flag)
    app.exec_()