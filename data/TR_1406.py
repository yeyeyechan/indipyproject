

# -*- coding: utf-8 -*-
import sys
import os
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from time import sleep
from pymongo import MongoClient
from datetime import datetime
from log.logger_pyflask import logging_instance
from analysis.common_data import common_min_shortTime
import telegram


class TR_1406(QMainWindow):
    def __init__(self, market, day, gubun):
        super().__init__()
        #logging
        self.realTimeLogger = logging_instance("TR_1406.py_ PID: "+(str)(self.processID)).mylogger
        #telegram
        telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
        self.bot = telegram.Bot(token=telgm_token)

        #db
        db_name = str(datetime.today().strftime("%Y%m%d"))
        collection_name = "TR_1406_"+db_name
        client = MongoClient('127.0.0.1', 27017)
        db = client[db_name]
        self.collection = db[collection_name]
        self.realTimeLogger("TR_1406 OCX call")
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.realTimeLogger("TR_1406 OCX call end")

        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.market = market
        self.gubun = gubun
        self.day = day
        self.column = ['단축코드      ' ,
'장구분       ' ,
'한글종목명     ' ,
'현재가       ' ,
'전일대비구분    ' ,
'전일대비      ' ,
'전일대비율     ' ,
'외국인누적거래량  ' ,
'외국인보유비중   ' ,
'기관누적거래량   ' ,
'발행수량      ' ,
'외국인보유     '

]
        self.realTimeLogger("TR_1406 input setup before")

        self.setup()
    def setup(self):
        self.realTimeLogger = logging_instance("TR_1406.py_   setup   PID: "+(str)(self.processID)).mylogger

        # 조회할 종목의 이름을 받아옵니다.
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "TR_1406")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.market)  # 인풋 : 시장구분 0 코스피 1 코스닥 2 전체
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1,self.day)  # 인풋 : 상하한구분 1 상한가 4 하한가
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, self.gubun)  # 인풋 : 날짜 YYYYMMDD

        rqid = self.IndiTR.dynamicCall("RequestData()")
        self.realTimeLogger("TR_1406 input setup finished  RequestData")

    def ReceiveData(self, rqid):

        self.realTimeLogger = logging_instance("TR_1406.py_   received DATA   PID: "+(str)(self.processID)).mylogger

        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        for i in range(0, nCnt):
            # 데이터 양식

            DATA = {}
            DATA[self.column[0].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 0) #단축코드
            self.realTimeLogger.info(DATA)
            self.realTimeLogger(self.collection1.insert_one(DATA))
            sleep(0.5)
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    TR_1406_vari =TR_1406(2,2,1)
    app.exec_()