

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
import telegram
import time

class TR_1406(QMainWindow):
    def __init__(self, market, day, gubun):
        super().__init__()
        #logging
        self.processID =os.getpid()
        self.realTimeLogger = logging_instance("TR_1406 실행 합니다  Process ID 는 :  "+(str)(self.processID)).mylogger
        #telegram
        telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
        self.bot = telegram.Bot(token=telgm_token)

        #db
        db_name = str(datetime.today().strftime("%Y%m%d"))
        db_name = "20200311"
        collection_name = "TR_1406_"+db_name
        client = MongoClient('127.0.0.1', 27017)
        db = client[db_name]
        self.TR_1406 = db[collection_name]


        self.realTimeLogger.info("TR_1406 OCX call")
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.realTimeLogger.info("TR_1406 OCX call end")

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
        self.realTimeLogger.info("TR_1406 input setup before")

        self.setup()
    def setup(self):
        self.realTimeLogger = logging_instance("TR_1406.py_   setup   PID: "+(str)(self.processID)).mylogger

        # 조회할 종목의 이름을 받아옵니다.
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "TR_1406")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.market)  # 인풋 : 시장구분 0 코스피 1 코스닥 2 전체
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1,self.day)  #예 :“3”= 전영업일 기준 3일 연속 순매수/순매도( 최소값 : 1 )
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, self.gubun)  # 1 순매수 2 순매도
        rqid = self.IndiTR.dynamicCall("RequestData()")
        self.realTimeLogger.info("TR_1406 input setup finished  RequestData")

    def ReceiveData(self, rqid):

        self.realTimeLogger = logging_instance("TR_1406.py_   received DATA   PID: "+(str)(self.processID)).mylogger
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        for i in range(0, nCnt):
            # 데이터 양식
            DATA = {}
            DATA['단축코드'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 0)
            DATA['종목명'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 2)
            DATA['구분코드'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 4)
            if DATA['구분코드'] =="5":
                DATA['구분'] ="전일 하락"
            if DATA['구분코드'] == "2":
                DATA['구분'] = "전일 상승"
            if DATA['구분코드'] == "3":
                DATA['구분'] = "전일 보합"
            self.TR_1406.insert_one(DATA)
            self.realTimeLogger.info('TR_1406 데이터 저장  '+str(DATA))

        return
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tr_1406_vari = TR_1406("2", "1","1")
    app.exec_()