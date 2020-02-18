'''
TRAM-ID : SK
TR 내용 : 현물 거래원

INPUT FIELD
[Single 데이터】
Field#	항 목 명	SIZE	항 목 내 용 설 명

0	   단축코드	     6


'''

# -*- coding: utf-8 -*-
import sys
import time
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from time import sleep
import requests
from pymongo import MongoClient
import datetime
from datetime import timedelta
from data.common import mongo_find
import json
from data.TR_1206 import TR_1206
class SK(QMainWindow):
    def __init__(self, stock_code):
        super().__init__()
        # 인디의 TR을 처리할 변수를 생성합니다.
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")


        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)

        self.stock_code= stock_code

        self.btn_Search()

    # 그럼 실제로 과거 주가를 받아오는 부분은 다음과 같습니다.
    def btn_Search(self):

        # 차트조회 : 과거주가는 차트조회를 통해 받아올 수 있습니다.
        # TR_SCHART : 과거주가를 요청할 TR입니다.
        # 해당 TR의 필드입력형식에 맞춰서 TR을 날리면 됩니다.
        # 데이터 요청 형식
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "SK")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.stock_code) # 단축코드
        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청
    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        stock_data =['체결시간' , '국내총순매수대금', '외국계총순매수대금', '전체순매수대금', '단축코드']

        # 데이터 양식
        DATA = {}

        print(self.IndiTR.dynamicCall("GetSingleData(int)", 0) )
        # 데이터 받기
        DATA[stock_data[0]] = self.IndiTR.dynamicCall("GetSingleData(int)", 2)  # 체결시간
        DATA[stock_data[1]] = self.IndiTR.dynamicCall("GetSingleData(int)", 42)  # 국내총순매수대금
        DATA[stock_data[2]] = self.IndiTR.dynamicCall("GetSingleData(int)", 48)  # 외국계총순매수대금
        DATA[stock_data[3]] = self.IndiTR.dynamicCall("GetSingleData(int)", 54)  # 전체순매수대금
        DATA[stock_data[4]] = self.IndiTR.dynamicCall("GetSingleData(int)", 1)  # 단축코드
        rqid = self.IndiTR.dynamicCall("ClearReceiveBuffer()") # 데이터 요청

        print("SK")
        print(DATA)
        print("SK")
        print( DATA[stock_data[2]] is not '' and DATA[stock_data[1]] is not '')
        if  DATA[stock_data[2]]is not '' and DATA[stock_data[1]] is not '':
            if int(DATA[stock_data[2]])>0 and  int(DATA[stock_data[1]])<0 :
                TR_1206_vari = TR_1206(DATA[stock_data[4]], "20200113", "20200114", "1", "1")
                time.sleep(1)
                return
            print("check1")
        print("check2")
        return
        #client = MongoClient('127.0.0.1', 27017)
        #db = client["stock_data"]
        #collection = db["SK"]
        #print(collection.insert(DATA))
        #time.sleep(0.5)
        #QCoreApplication.instance().quit()


    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    client = MongoClient('127.0.0.1', 27017)
    db = client["stock_data"]
    collection = db["stock_mst"]
    app = QApplication(sys.argv)

    for i in collection.find():
        SK_vari = SK(i["단축코드"])
        time.sleep(0.5)
    app.exec_()
