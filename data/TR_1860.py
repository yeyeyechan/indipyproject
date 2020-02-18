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


class TR_1860(QMainWindow):
    def __init__(self, market, division, date, volume, condition, total_volume):
        super().__init__()

        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)


        self.market = market
        self.division = division
        self.date = date
        self.volume = volume
        self.condition = condition
        self.total_volume = total_volume
        self.stock_data = {
            'stock_code': [],
            'korName' : [],
            'dayEndPrice': [],
            'curPrice': [],
            'diff'               : [],
            'diffPrice'          : [],
            'diffPercent'        : [],
            'Enddiff'            : [],
            'EnddiffPrice'       : [],
            'EnddiffPercent'     : [],
            'conDay'             : [],
            'exStr'              : [],
            'cumVol'             : [],
            'busiIndex'          : [],
            'sellPriceAllCount'  : [],
            'buyPriceAllCount'   : [],
            'sellPrice'          : [],
            'buyPrice'           : [],
            'sellPriceCount'     : [],
            'buyPriceCount'      : [],
            'date'               : []
        }
        self.btn_Search()
    def btn_Search(self):
        # 조회할 종목의 이름을 받아옵니다.
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "TR_1860")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.market)  # 인풋 : 시장구분 0 코스피 1 코스닥 2 전체
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1,self.division)  # 인풋 : 상하한구분 1 상한가 4 하한가
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, self.date)  # 인풋 : 날짜 YYYYMMDD
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3, self.volume)  # 인풋 : 거래량조건 주 (1)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 4,  self.condition)  # 인풋 : 종목조건
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 5,  self.total_volume)  # 인풋 : 시가총액조건
        rqid = self.IndiTR.dynamicCall("RequestData()")
        print("rqid")
        print(rqid)
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.

        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        print(nCnt)

        for i in range(0, nCnt):
            # 데이터 양식
            DATA = {}
            DATA['stock_code'          ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 0)
            DATA['korName'          ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 1)
            DATA['dayEndPrice'      ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 2)
            DATA['curPrice'         ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 2)
            DATA['diff'             ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 4)
            DATA['diffPrice'        ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 5)
            DATA['diffPercent'      ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 6)
            DATA['Enddiff'          ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 7)
            DATA['EnddiffPrice'     ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 8)
            DATA['EnddiffPercent'   ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 9)
            DATA['conDay'           ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 10)
            DATA['exStr'            ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 11)
            DATA['cumVol'           ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 12)
            DATA['busiIndex'        ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 13)
            DATA['sellPriceAllCount'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 14)
            DATA['buyPriceAllCount' ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 15)
            DATA['sellPrice'        ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 16)
            DATA['buyPrice'         ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 17)
            DATA['sellPriceCount'   ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 18)
            DATA['buyPriceCount'    ] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 19)
            DATA['date'             ] = self.date
            DATA['market'             ] = self.market
            self.stock_data['stock_code'].append(DATA['stock_code'])
            self.stock_data['korName'].append(DATA['korName'])
            self.stock_data['dayEndPrice'].append(DATA['dayEndPrice'])
            self.stock_data['curPrice'].append(DATA['curPrice'])
            self.stock_data['diff'].append(DATA['diff'])
            self.stock_data['diffPrice'].append(DATA['diffPrice'])
            self.stock_data['diffPercent'].append(DATA['diffPercent'])
            self.stock_data['Enddiff'].append(DATA['Enddiff'])
            self.stock_data['EnddiffPrice'].append(DATA['EnddiffPrice'])
            self.stock_data['EnddiffPercent'].append(DATA['EnddiffPercent'])
            self.stock_data['conDay'].append(DATA['conDay'])
            self.stock_data['exStr'].append(DATA['exStr'])
            self.stock_data['cumVol'].append(DATA['cumVol'])
            self.stock_data['busiIndex'].append(DATA['busiIndex'])
            self.stock_data['sellPriceAllCount'].append(DATA['sellPriceAllCount'])
            self.stock_data['buyPriceAllCount'].append(DATA['buyPriceAllCount'])
            self.stock_data['sellPrice'].append(DATA['sellPrice'])
            self.stock_data['buyPrice'].append(DATA['buyPrice'])
            self.stock_data['sellPriceCount'].append(DATA['sellPriceCount'])
            self.stock_data['buyPriceCount'].append(DATA['buyPriceCount'])
            self.stock_data['date'].append(DATA['date'])
            print(DATA)
            client = MongoClient('127.0.0.1', 27017)
            #db = client["stock_data"]
            db = client["test_stock_data"]
            #collection = db["test_TR_1860"]
            collection = db["TR_1860"]
            print(collection.insert(DATA))
            sleep(0.5)
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start = datetime.datetime(2019,1,1)
    end = datetime.datetime(2019,11,23)
    delta = timedelta(days =1)

    day = start
    diff = 0
    while day <= end:
        if weekday_check(day):
            input_day = day.strftime("%Y%m%d")
            activate_Tr= TR_1860('2', '1', input_day , '1', '1', '1')
            sleep(1)
        day += delta
    app.exec_()