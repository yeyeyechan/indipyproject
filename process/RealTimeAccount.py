'''
TRAM-ID : AD


'''

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")

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
import telegram

class RealTimeAccount(QMainWindow):
    def __init__(self):
        super().__init__()
        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

        telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
        self.bot = telegram.Bot(token=telgm_token)
        self.realTimeLogger = logging_instance("RealTimeAccount.py 현물 실시간 주문 체결").mylogger
        self.timeline = common_min_shortTime(5).timeline
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)

        # 인디의 TR을 처리할 변수를 생성합니다.

        self.client = MongoClient('127.0.0.1', 27017)
        db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
        self.db = self.client[db_name]
        self.collection_name1 = "AD_" + db_name
        self.collection1 = self.db [self.collection_name1]

        self.realTimeLogger.info("RealTimeAccount  AD UnRequestRTReg 호출")

        ret1 = self.indiReal.dynamicCall("UnRequestRTReg(QString, QString)", "AD", "*")
        if ret1 :
            self.realTimeLogger.info("UnRequestRTReg  AD 완료")
            self.realTimeLogger.info("UnRequestRTReg  return 값 : " + str(ret1))
        else :
            self.realTimeLogger.error("UnRequestRTReg  AD 실패")
            self.realTimeLogger.error("UnRequestRTReg  return 값 : " + str(ret1))
            self.realTimeLogger.info("RealTimeAccount AD RequestRTReg 호출")
        ret2 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "AD", "*")
        if ret2 :
            self.realTimeLogger.info("RequestRTReg  AD완료")
            self.realTimeLogger.info("RequestRTReg  return 값 : " + str(ret2))
        else :
            self.realTimeLogger.error("RequestRTReg AD 실패")
            self.realTimeLogger.error("RequestRTReg  return 값 : " + str(ret2))

        self.realTimeLogger.info("RealTimeAccount  init() 완료")


    def ReceiveRTData(self, rqid):
        self.realTimeLogger = logging_instance("RealTimeAccount.py 현물 실시간 주문 체결").mylogger
        DATA ={

        }
        print(rqid)
        if rqid == "AD":
            self.realTimeLogger.info("rqid is  AD")
            DATA['종목명'] = self.indiReal.dynamicCall("GetSingleData(int)", 4)
            DATA['평가금액'] = self.indiReal.dynamicCall("GetSingleData(int)", 2)
            DATA['평가손익'] = self.indiReal.dynamicCall("GetSingleData(int)", 11)
            DATA['총평가금액'] = self.indiReal.dynamicCall("GetSingleData(int)", 19)
            self.realTimeLogger.info("AD data received")
            self.collection1.insert_one(DATA)
            self.realTimeLogger.info("AD  data saved to mongoDB")
            message = "종목명 :  "+DATA['종목명'] +"   평가금액 :  "+DATA['평가금액'] +"    평가손익  :  "+DATA['평가손익'] +"    총평가금액 :  "+DATA['총평가금액']
            self.bot.sendMessage(chat_id='813531834', text=message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    activate_Tr = RealTimeAccount()
    app.exec_()
