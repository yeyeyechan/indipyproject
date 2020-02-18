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
import numpy as np

'''
    신한아이 인디 국내주식 날짜별 상한가 종목 조회
'''

class IndiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IndiExample")

       # 실시간 TR OCX
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.IndiTR.ReceiveData.connect(self.ReceiveData) # 실시간 TR에 대한 응답을 받는 함수를 연결해줍니다.

        # TR ID를 저장해놓고 처리할 딕셔너리 생성
        self.rqidD = {}

        # PyQt5를 통해 화면을 그려주는 코드입니다.
        self.MainSymbol = ""
        self.setGeometry(800, 400, 300, 150)

        label1 = QLabel("시장구분", self)
        label1.move(20, 20)
        # LineEdit
        self.lineEdit1 = QLineEdit("", self)
        self.lineEdit1.move(80, 20)

        label2 = QLabel("상하한구분", self)
        label2.move(20, 40)
        # LineEdit
        self.lineEdit2 = QLineEdit("", self)
        self.lineEdit2.move(80, 40)

        label3 = QLabel("날짜", self)
        label3.move(20, 60)
        # LineEdit
        self.lineEdit3 = QLineEdit("", self)
        self.lineEdit3.move(80, 60)

        label4 = QLabel("거래량조건", self)
        label4.move(20, 80)
        # LineEdit
        self.lineEdit4 = QLineEdit("", self)
        self.lineEdit4.move(80, 80)

        label5 = QLabel("종목조건", self)
        label5.move(20, 100)
        # LineEdit
        self.lineEdit5 = QLineEdit("", self)
        self.lineEdit5.move(80, 100)

        label6 = QLabel("시가총액조건", self)
        label6.move(20, 120)
        # LineEdit
        self.lineEdit6 = QLineEdit("", self)
        self.lineEdit6.move(80, 120)

        # PyQt5를 통해 버튼만들고 함수와 연결시킵니다.
        btnResearch = QPushButton("Search", self)
        btnResearch.setGeometry(85, 20, 50, 20)
        btnResearch.clicked.connect(self.btn_Search)  # 버튼을 누르면 'btn_Search' 함수가 실행됩니다.

    # 버튼을 누르면 일반TR로 현재가 조회를 먼저 요청을 합니다.
    def btn_Search(self):
        # 조회할 종목의 이름을 받아옵니다.
        market = self.lineEdit1.text()
        self.market = market
        print(market)

        upperLower = self.lineEdit2.text()
        self.upperLower = upperLower
        print(upperLower)

        date8 = self.lineEdit3.text()
        self.date8 = date8
        print(date8)

        volumeCondition = self.lineEdit4.text()
        self.volumeCondition = volumeCondition
        print(volumeCondition)

        stockCondition = self.lineEdit5.text()
        self.stockCondition = stockCondition
        print(stockCondition)

        markeCapCon = self.lineEdit6.text()
        self.markeCapCon = markeCapCon
        print(markeCapCon)

        # 종목 현재가 조회, 일반TR로 요청합니다. 바로 실시간 TR을 등록해도 상관없습니다.
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "TR_1860")
        print(ret)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.market) # 인풋 : 시장구분
        print(ret)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1, self.upperLower) # 인풋 : 상하한구분
        print(ret)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, self.date8) # 인풋 : 날짜
        print(ret)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3, self.volumeCondition) # 인풋 : 거래량조건
        print(ret)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 4, self.stockCondition) # 인풋 : 종목조건
        print(ret)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 5, self.markeCapCon) # 인풋 : 시가총액조건
        print(ret)

        rqid = self.IndiTR.dynamicCall("RequestData()")
        print(rqid)

        self.rqidD[rqid] = "TR_1860"
        if(rqid==0):
            print("call Fail")
        else:
            print("call Success")

    def ReceiveData(self, rqid):

        TRName = self.rqidD[rqid]
        DATA = {}

        if TRName == "TR_1860" :
            # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
            nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")

            output1 =[]
            output2 =[]
            output3 =[]
            output4 =[]
            output5 =[]
            output6 =[]
            output7 =[]
            output8 =[]
            output9 =[]
            output10 =[]
            output11 =[]
            output12 =[]
            output13 =[]
            output14 =[]
            output15 =[]
            output16=[]
            output17 =[]
            output18 =[]
            output19 =[]
            # 받을 열만큼 가거 데이터를 받도록 합니다.
            for i in range(0, nCnt):
                # 데이터 양식
                DATA1 = {}

                # 데이터 받기
                DATA1['DATE'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 0)  # 일자
                DATA1['TIME'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 1)  # 시간
                DATA1['OPEN'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 2)  # 시가
                DATA1['HIGH'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 3)  # 고가
                DATA1['Low'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 4)  # 저가
                DATA1['Close'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 5)  # 종가
                DATA1['Price_ADJ'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 6)  # 주가수정계수
                DATA1['Vol_ADJ'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 7)  # 거래량 수정계수
                DATA1['Rock'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 8)  # 락구분
                DATA1['Vol'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 9)  # 단위거래량
                DATA1['Trading_Value'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 10)  # 단위거래대금
                print(DATA1)
                # 데이터 받기
                output1.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 1)) # 한글종목명
                output2.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 2)) # 해당일종가
                output3.append( self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 3) ) # 현재가
                output4.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 4))  # 전일대비구분
                output5.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 5)) # 전일대비
                output6.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 6))  # 전일대비율
                output7.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 7))  # 종가 전일대비구분
                output8.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 8))  # 종가 전일대비
                output9.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 9))  # 종가 전일대비율
                output10.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 10))  # 연속일
                output11.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 11))  # 거래강도
                output12.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 12))  # 누적거래량
                output13.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 13))  # 업종구분
                output14.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 14))  # 매도 총호가수량
                output15.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 15))  # 매도 총호가수량
                output16.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 16))  # 매도1호가
                output17.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 17))  # 매도1호가
                output18.append(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 18))  # 매도1호가 수량
                output19.append( self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 19))  # 매도1호가 수량

            DATA['korName']=output1
            DATA['dayEndPrice']=output2
            DATA['curPrice']=output3
            DATA['diff']=output4
            DATA['diffPrice']=output5
            DATA['diffPercent']=output6
            DATA['Enddiff']=output7
            DATA['EnddiffPrice']=output8
            DATA['EnddiffPercent']=output9
            DATA['conDay']=output10
            DATA['exStr']=output11
            DATA['cumVol']=output12
            DATA['busiIndex']=output13
            DATA['sellPriceAllCount']=output14
            DATA['buyPriceAllCount']=output15
            DATA['sellPrice']=output16
            DATA['buyPrice']=output17
            DATA['sellPriceCount']=output18
            DATA['buyPriceCount']=output19

        df = pd.DataFrame(DATA)
        df.to_csv('testData.csv', encoding="utf-8-sig")
        self.rqidD.__delitem__(rqid)
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    IndiWindow = IndiWindow()
    IndiWindow.show()
    app.exec_()