'''
PROTOCOL
TRAN-ID	TR_1860	TR구분	XMFTR
	TR 내용	상한가/하한가 종목 조회

INPUT FIELD
Field#	항 목 명	SIZE	항 목 내 용 설 명
【Single 데이터】
0	시장구분	1	0 : KOSPI, 1 : KOSDAQ, 2 : 전체
1	상하한구분	3	1 : 상한가, 4 : 하한가
2	날짜	8	YYYYMMDD
3	거래량조건	15	단위:주
4	종목조건	1	1:전체조회 2:관리종목제외 3:증거금100%인 종목제외 A:증거금20%인 종목보기 B:증거금30%인 종목보기 C:증거금40%인 종목보기 D:증거금100%인 종목보기
5	시가총액조건	8	단위:억

'''

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


class TR_1205(QMainWindow):
    def __init__(self, sectorCode, startDate, endDate):
        super().__init__()

        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.sectorCode = sectorCode
        self.startDate = startDate
        self.endDate = endDate
        self.column = ['한글업종명             ' ,
'개인매수              ' ,
'개인매도              ' ,
'개인순매수             ' ,
'외국인매수             ' ,
'외국인매도             ' ,
'외국인순매수            ' ,
'기관매수              ' ,
'기관매도              ' ,
'기관순매수             ' ,
'증권매수              ' ,
'증권매도              ' ,
'증권순매수             ' ,
'투신매수              ' ,
'투신매도              ' ,
'투신순매수             ' ,
'은행매수              ' ,
'은행매도              ' ,
'은행순매수             ' ,
'종금매수              ' ,
'종금매도              ' ,
'종금순매수             ' ,
'보험매수              ' ,
'보험매도              ' ,
'보험순매수             ' ,
'기금매수              ' ,
'기금매도              ' ,
'기금순매수             ' ,
'기타매수              ' ,
'기타매도              ' ,
'기타순매수             ' ,
'외국인기타매수           ' ,
'외국인기타매도           ' ,
'외국인기타순매수          ' ,
'외국인계매수            ' ,
'외국인계매도            ' ,
'외국인계순매수           ' ,
'국가매수거래대금          ' ,
'국가매도거래대금          ' ,
'국가순매수거래대금         '
]
        self.btn_Search()

    def btn_Search(self):
        # 조회할 종목의 이름을 받아옵니다.
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "TR_1205")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.sectorCode)  # 인풋 : 시장구분 0 코스피 1 코스닥 2 전체
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1,self.startDate)  # 인풋 : 상하한구분 1 상한가 4 하한가
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, self.endDate)  # 인풋 : 날짜 YYYYMMDD
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3,"K")  # 인풋 : 거래량조건 주 (1)
        rqid = self.IndiTR.dynamicCall("RequestData()")
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.

        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        print(nCnt)

        for i in range(0, nCnt):
            # 데이터 양식
            DATA = {}
            DATA[self.column[0].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 0).strip() #한글업종명
            DATA[self.column[3].strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 3)) #개인순매수
            DATA[self.column[6].strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 6)) #외국인순매수
            DATA[self.column[9].strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 9)) #기관순매수


            print(DATA)
            client = MongoClient('127.0.0.1', 27017)
            db = client["stock_data"]
            #db = client["test_stock_data"]
            #collection = db["test_TR_1860"]
            collection_name = "TR_1205"+"_4"
            collection = db[collection_name]
            print(collection.insert(DATA))
            sleep(0.5)
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #activate_Tr= TR_1205('1', '20200113', "20200116" )
    activate_Tr= TR_1205('0', '20200113', "20200116" )
    app.exec_()