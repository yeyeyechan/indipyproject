

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
import time

class TR_1314_3(QMainWindow):
    def __init__(self, date):
        super().__init__()

        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.date = date
        self.column =[
            '종목명                           ',
            '단축코드                          ',
            '현재가                           ',
            '등락구분                          ',
            '등락                            ',
            '등락율                           ',
            '당일누적거래량                       ',
            '당일누적거래대금                      ',
            '누적거래량(외국인 외국계 창구포함)           ',
            '누적거래량(투신)                     ',
            '누적거래량(은행)                     ',
            '누적거래량(보험/종금)                  ',
            '누적거래량(기금, 공제)                 ',
            '누적거래량(기타법인)                   ',
            '누적거래량(국가/지자체)                 ',
            '프로그램매수수량                      '
        ]
        self.btn_Search()
    def btn_Search(self):
        # 조회할 종목의 이름을 받아옵니다.
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "TR_1314_3")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, '09')  # 인풋 : 시장구분 0 코스피 1 코스닥 2 전체
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1,'2')  # 인풋 : 상하한구분 1 상한가 4 하한가
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, '0')  # 인풋 : 날짜 YYYYMMDD
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3, '1')  # 인풋 : 날짜 YYYYMMDD
        rqid = self.IndiTR.dynamicCall("RequestData()")
        print(rqid)
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        client = MongoClient('127.0.0.1', 27017)
        db = client[self.date]
        collection1 = db["TR_1314_3_3"] #상승
        collection2 = db["TR_1314_3_2"] #보합
        collection3 = db["TR_1314_3_5"] #하락
        collection_status = db["TR_1314_status"]
        collection_status_param = {
            "status": "Processing"
        }
        if collection_status.find():
            collection_status.insert(collection_status_param)
        else:
            for i in collection_status.find():
                try:
                    if i["status"] != "":
                        collection_status.update({
                            "status": i["status"]
                        }, {
                            "status": "Processing"
                        })
                        break
                    else:
                        collection_status.insert(collection_status_param)
                except Exception:
                    print(Exception)
                    QCoreApplication.exit(0)

        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        print(nCnt)
        try:
            for i in range(0, nCnt):
                # 데이터 양식
                DATA = {}
                if self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 3) == '5':
                    DATA[self.column[0].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 0)
                    DATA[self.column[1].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 1)
                    DATA["구분"] = "전일 하락"
                    DATA["구분코드"] = "5"
                    print(collection3.insert(DATA))
                    sleep(0.05)
                if self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 3) == '2':
                    DATA[self.column[0].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 0)
                    DATA[self.column[1].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 1)
                    DATA["구분"] = "전일 보합"
                    DATA["구분코드"] = "2"

                    print(collection2.insert(DATA))
                    sleep(0.05)
                if self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 3) == '3':
                    DATA[self.column[0].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 0)
                    DATA[self.column[1].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 1)
                    DATA["구분"] = "전일 상승"
                    DATA["구분코드"] = "3"
                    print(collection1.insert(DATA))
                    sleep(0.05)
        except Exception:
            collection_status.update(collection_status_param, {
                "status": "Fail"
            })
            collection_status_param['status']= "Fail"
            QCoreApplication.exit(0)
        collection_status.update(collection_status_param, {
            "status": "Success"
        })
        QCoreApplication.exit(0)
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    TR_1314_3_vari =TR_1314_3()
    app.exec_()