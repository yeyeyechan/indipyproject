'''
TRAM-ID : TR_SCHART
TR 내용 : 현물 분/일/주

INPUT FIELD
[Single 데이터】
Field#	항 목 명	SIZE	항 목 내 용 설 명

0	   단축코드	     6

1	   그래프종류	1	    1:분데이터 		D:일데이터
                            W:주데이터		M:월데이터

2	   시간간격	     3	    분데이터일 경우 1 – 30
                            일/주/월데이터일 경우 1

3	    시작일	     8	    YYYYMMDD
                            분 데이터 요청시 : “00000000”


4	    종료일	    8	    YYYYMMDD
                            분 데이터 요청시 : “99999999”

5	    조회갯수	    4	    1 – 9999

'''

# -*- coding: utf-8 -*-
import sys
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
from pymongo import MongoClient
import datetime
from data.common import  weekday_check
from datetime import timedelta
from data.common import mongo_find
import time
class realTimePrice(QMainWindow):
    def __init__(self, stock_code, korName , standard, term, start_date, end_date, counts,date):
        super().__init__()
        # 인디의 TR을 처리할 변수를 생성합니다.
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        print("start")
        print("counts    ")
        print(counts)
        print(stock_code)
        print(korName)
        print(standard)
        print(term)
        print(start_date)
        print(end_date)
        print(counts)
        print("counts    ")
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.korName= korName
        self.stock_code= stock_code
        self.standard= standard
        self.term= term
        self.start_date= start_date
        self.end_date= end_date
        self.counts= counts
        self.date= date

        self.client = MongoClient('127.0.0.1', 27017)
        db_name =self.date
        #db_name = "20200214"
        self.db = self.client[db_name]
        self.collection_name = "TR_SCHART_" + db_name
        self.collection = self.db [self.collection_name]

        #self.market = market
        self.btn_Search()



        print("start2")

    # 그럼 실제로 과거 주가를 받아오는 부분은 다음과 같습니다.
    def btn_Search(self):

        # 차트조회 : 과거주가는 차트조회를 통해 받아올 수 있습니다.
        # TR_SCHART : 과거주가를 요청할 TR입니다.
        # 해당 TR의 필드입력형식에 맞춰서 TR을 날리면 됩니다.
        # 데이터 요청 형식
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "TR_SCHART")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.stock_code) # 단축코드
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1, self.standard) # 1:분봉, D:일봉, W:주봉, M:월봉
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2,   self.term) # 분봉: 1~30, 일/주/월 : 1
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3, self.start_date) # 시작일(YYYYMMDD)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 4, self.end_date) # 종료일(YYYYMMDD)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 5, self.counts) # 조회갯수(1~9999)
        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청
        print("btn_search")
    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        print("receive Data")
        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        print(nCnt)
        stock_data ={
            'DATE': [],
            'TIME': [],
            'OPEN': [],
            'HIGH': [],
            'Low': [],
            'Close': [],
            'Price_ADJ': [],
            'Vol_ADJ': [],
            'Rock': [],
            'Vol': [],
            'Trading_Value': [],
            'start_date': [],
            'end_date': [],
            'market': [],
        }
        # 받을 열만큼 가거 데이터를 받도록 합니다.
        for i in range(0, nCnt):
            # 데이터 양식
            DATA = {}

            # 데이터 받기
            DATA['DATE'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 0)  # 일자
            DATA['TIME'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 1)  # 시간
            DATA['OPEN'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 2)  # 시가
            DATA['HIGH'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 3)  # 고가
            DATA['Low'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 4)  # 저가
            DATA['Close'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 5)  # 종가
            DATA['Price_ADJ'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 6)  # 주가수정계수
            DATA['Vol_ADJ'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 7)  # 거래량 수정계수
            DATA['Rock'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 8)  # 락구분
            DATA['Vol'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 9)  # 단위거래량
            DATA['Trading_Value'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 10)  # 단위거래대금

            DATA['stock_code'] = self.stock_code # 주식코드
            DATA['korName'] = self.korName.strip() # 한글 이름
            #DATA['start_date'] = self.start_date # 시작일
            #DATA['end_date'] = self.end_date  # 마지막일
            #DATA['market'] = self.market # market


            stock_data['DATE'].append(DATA['DATE'])
            stock_data['TIME'].append(DATA['TIME'])
            stock_data['OPEN'].append(DATA['OPEN'])
            stock_data['HIGH'].append(DATA['HIGH'])
            stock_data['Low'].append(DATA['Low'])
            stock_data['Close'].append(DATA['Close'])
            stock_data['Price_ADJ'].append(DATA['Price_ADJ'])
            stock_data['Vol_ADJ'].append(DATA['Vol_ADJ'])
            stock_data['Rock'].append(DATA['Rock'])
            stock_data['Vol'].append(DATA['Vol'])
            stock_data['Trading_Value'].append(DATA['Trading_Value'])
            print(DATA)

            if self.collection.find_one({'stock_code':  self.stock_code, 'TIME':  DATA['TIME'] }):
                self.collection.update(self.collection.find_one({'stock_code':  self.stock_code, 'TIME':  DATA['TIME'] }), DATA, upsert=True)
            else:
                self.collection.insert(DATA)
            #self.collection.insert(DATA)
            #time.sleep(0.3)
            #db = client["20200206"]
            #collection_name = "TR_SCHART_20200206"
            '''if DATA['DATE'] == str(datetime.datetime.today().strftime("%Y%m%d")):
                collection = db[collection_name]
                collection.update(
                        DATA, DATA, upsert =True
                )
                print("Success")
                time.sleep(0.3)'''
        QCoreApplication.instance().exit(0)

    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    activate_Tr = realTimePrice("005690", "대창", '1', '5', "00000000", "99999999",  "78")
    app.exec_()
