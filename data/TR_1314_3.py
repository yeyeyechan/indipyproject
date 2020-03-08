'''
    전일 기준 외국인/기관 매수 종목 검색


'''

# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from time import sleep

from pymongo import MongoClient
class TR_1314_3(QMainWindow):
    def __init__(self, date):
        super().__init__()
        client = MongoClient('127.0.0.1', 27017)
        self.date = date
        db = client[self.date]
        self.collection1 = db["TR_1314_3_3"] #보합
        self.collection2 = db["TR_1314_3_2"] #상승
        self.collection3 = db["TR_1314_3_5"] #하락

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
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, '09')  # 09 외국인
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1,'2')  # 2 전체
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, '0')  # 상위
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3, '1')  # 1 매수
        rqid = self.IndiTR.dynamicCall("RequestData()")

    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.

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
                    print(self.collection3.insert(DATA))
                    sleep(0.05)
                if self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 3) == '2':
                    DATA[self.column[0].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 0)
                    DATA[self.column[1].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 1)
                    DATA["구분"] = "전일 상승"
                    DATA["구분코드"] = "2"
                    print(self.collection2.insert(DATA))
                    sleep(0.05)
                if self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 3) == '3':
                    DATA[self.column[0].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 0)
                    DATA[self.column[1].strip()] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 1)
                    DATA["구분"] = "전일 보합"
                    DATA["구분코드"] = "3"
                    print(self.collection1.insert(DATA))
                    sleep(0.05)
        except Exception:
            QCoreApplication.exit(0)
        QCoreApplication.exit(0)
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    TR_1314_3_vari =TR_1314_3(sys.argv[1])
    app.exec_()