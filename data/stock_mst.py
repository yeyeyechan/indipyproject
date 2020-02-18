'''


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
class stock_mst(QMainWindow):
    def __init__(self):
        super().__init__()
        # 인디의 TR을 처리할 변수를 생성합니다.
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")


        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.btn_Search()

    # 그럼 실제로 과거 주가를 받아오는 부분은 다음과 같습니다.
    def btn_Search(self):

        # 차트조회 : 과거주가는 차트조회를 통해 받아올 수 있습니다.
        # TR_SCHART : 과거주가를 요청할 TR입니다.
        # 해당 TR의 필드입력형식에 맞춰서 TR을 날리면 됩니다.
        # 데이터 요청 형식
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "stock_mst")
        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청
    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        print(nCnt)
        column = [
            '표준코드               ',
            '단축코드               ',
            '장구분                ',
            '종목명                ',
            'KOSPI200 세부업종      ',
            '결산월일               ',
            '거래정지구분             ',
            '관리구분               ',
            '시장경보구분코드           ',
            '락구분                ',
            '불성실공시지정여부          ',
            '증거금 구분             ',
            '신용증거금 구분           ',
            'ETF 구분자            ',
            '소속구분               '

        ]
        client = MongoClient('127.0.0.1', 27017)
        # db = client["test_stock_data"]
        db = client["stock_data"]
        collection = db["stock_mst"]

        # 받을 열만큼 가거 데이터를 받도록 합니다.
        for i in range(0, nCnt):
            # 데이터 양식
            DATA = {}

            DATA[column[0].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 0)
            DATA[column[1].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 1)
            DATA[column[2].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 2)
            DATA[column[3].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 3)
            DATA[column[4].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 4)
            DATA[column[5].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 5)
            DATA[column[6].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 6)
            DATA[column[7].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 7)
            DATA[column[8].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 8)
            DATA[column[9].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 9)
            DATA[column[10].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 10)
            DATA[column[11].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 11)
            DATA[column[12].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 12)
            DATA[column[13].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 13)


            #collection = db["test_TR_SCHART"]
            print(collection.insert(DATA))
            time.sleep(0.5)




    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stock_mst_val = stock_mst()

    app.exec_()
