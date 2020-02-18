

# -*- coding: utf-8 -*-
import sys
from datetime import timedelta

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from pandas import Series, DataFrame
import pandas as pd
from time import sleep
import threading
import numpy as np

from pytimekr import pytimekr
from pymongo import MongoClient
import datetime
from data.common import weekday_check


class TR_1864(QMainWindow):
    def __init__(self, market, gubun, debi, jogeon1, jogeon2):
        super().__init__()

        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)


        self.market = market
        self.gubun = gubun
        self.debi = debi
        self.jogeon1 = jogeon1
        self.jogeon2 = jogeon2
        self.column = ['순위           '   ,
'단축코드         '   ,
'한글종목명        '   ,
'현재가          '   ,
'전일대비구분       '   ,
'전일대비         '   ,
'전일대비율        '   ,
'누적거래량        '   ,
'급증률          '   ,
'매도1호가        '   ,
'매수1호가        '   ,
'업종구분         '
]
        self.btn_Search()
    def btn_Search(self):
        # 조회할 종목의 이름을 받아옵니다.
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "TR_1864")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.market)  # 인풋 : 시장구분 0 코스피 1 코스닥 2 전체
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1,self.gubun)  # 인풋 : 상하한구분 1 상한가 4 하한가
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, self.debi)  # 인풋 : 날짜 YYYYMMDD
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3, self.jogeon1)  # 인풋 : 거래량조건 주 (1)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 4,  self.jogeon2)  # 인풋 : 종목조건
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 5,  '0')  # 인풋 : 시가총액조건
        rqid = self.IndiTR.dynamicCall("RequestData()")
        print(rqid)
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.

        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        print(nCnt)

        for i in range(0, nCnt):
            # 데이터 양식
            DATA = {}
            DATA[self.column[0].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 0) #순위
            DATA[self.column[1].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 1) #단축코드
            DATA[self.column[2].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 2).strip() #한글종목명
            DATA[self.column[4].strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 4)) #전일대비구분
            DATA[self.column[5].strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 5) )#전일대비
            DATA[self.column[6].strip()] = float(self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 6)) #전일대비율
            DATA[self.column[8].strip()] = float(self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 8)) #급증률
            DATA[self.column[11].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 11) #업종구분


            print(DATA)
            client = MongoClient('127.0.0.1', 27017)
            db = client["stock_data"]
            #db = client["test_stock_data"]
            #collection = db["test_TR_1860"]
            collection = db["TR_1864_20200117"]
            print(collection.insert(DATA))
            sleep(0.5)
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    TR_1864_vari =TR_1864(2,1,3,1000, 1)
    app.exec_()