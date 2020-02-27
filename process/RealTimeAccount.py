'''
TRAM-ID : AD


'''

# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
import time
from pymongo import MongoClient
from log.logger_pyflask import logging_instance
from analysis.common_data import common_min_shortTime
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

class RealTimeAccount(QMainWindow):
    def __init__(self):
        super().__init__()
        self.realTimeLogger = logging_instance("RealTimeAccount.py 현물 실시간 주문 체결").mylogger
        self.timeline = common_min_shortTime(5).timeline
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)

        # 인디의 TR을 처리할 변수를 생성합니다.
        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

        self.client = MongoClient('127.0.0.1', 27017)
        db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
        self.db = self.client[db_name]
        self.collection_name1 = "AA_" + db_name
        self.collection1 = self.db [self.collection_name1]

        self.realTimeLogger.info("RealTimeAccount  AA UnRequestRTReg 호출")

        ret1 = self.indiReal.dynamicCall("UnRequestRTReg(QString, QString)", "AD", "*")
        if ret1 :
            self.realTimeLogger.info("UnRequestRTReg  AA 완료")
            self.realTimeLogger.info("UnRequestRTReg  return 값 : " + str(ret1))
        else :
            self.realTimeLogger.error("UnRequestRTReg  AA 실패")
            self.realTimeLogger.error("UnRequestRTReg  return 값 : " + str(ret1))
            self.realTimeLogger.info("RealTimeAccount  AA RequestRTReg 호출")
        ret2 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "AD", "*")
        if ret2 :
            self.realTimeLogger.info("RequestRTReg  AA 완료")
            self.realTimeLogger.info("RequestRTReg  return 값 : " + str(ret1))
        else :
            self.realTimeLogger.error("RequestRTReg  AA 실패")
            self.realTimeLogger.error("RequestRTReg  return 값 : " + str(ret1))

        self.realTimeLogger.info("RealTimeAccount  init() 완료")


    def ReceiveRTData(self, rqid):
        self.realTimeLogger = logging_instance("RealTimeAccount.py 현물 실시간 주문 체결").mylogger
        DATA ={

        }
        if rqid == "AA":
            self.realTimeLogger.info("rqid is   AA ")
            DATA['종목명'] = self.indiReal.dynamicCall("GetSingleData(int)", 4)
            DATA['평가금액'] = self.indiReal.dynamicCall("GetSingleData(int)", 2)
            DATA['평가손익'] = self.indiReal.dynamicCall("GetSingleData(int)", 11)
            DATA['총평가금액'] = self.indiReal.dynamicCall("GetSingleData(int)", 19)
            self.realTimeLogger.info("AA data received")
            self.collection1.insert_one(DATA)
            self.realTimeLogger.info("AA data saved to mongoDB")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    activate_Tr = RealTimeAccount()
    app.exec_()
