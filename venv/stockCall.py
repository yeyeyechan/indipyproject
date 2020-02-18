# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from pandas import Series, DataFrame
import pandas as pd
import numpy as np

class IndiWindow(QMainWindow):
    def __init__(self):
        super(IndiWindow, self).__init__()

        # QT 타이틀
        self.setWindowTitle("IndiExample")

        # 인디의 TR을 처리할 변수를 생성합니다.
        #self.IndiTR = QAxWidget("GIEXPERTCONTROL64.GiExpertControl64Ctrl.1")
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.rqidD = {} # TR 관리를 위해 사전 변수를 하나 생성합니다.

        # PyQt5를 통해 화면을 그려주는 코드입니다.
        self.MainSymbol = ""

        # PyQt5를 통해 버튼만들고 함수와 연결시킵니다.
        btnResearch = QPushButton("Search", self)
        btnResearch.setGeometry(20, 20, 50, 20)
        btnResearch.clicked.connect(self.btn_Search) # 버튼을 누르면 'btn_Search' 함수가 실행됩니다.

    # 생성한 버튼을 눌렀을 때 전 종목코드 조회가 나가도록 설정해줍니다.
    def btn_Search(self):
        # stock_mst : 주식 종목코드 조회를 요청할 TR입니다.
        # 해당 TR의 필드입력형식에 맞춰서 TR을 날리면 됩니다.
        # 데이터 요청 형식은 다음과 같습니다.
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "stock_mst")
        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청
        self.rqidD[rqid] =  "stock_mst"

    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        TRName = self.rqidD[rqid]

        # 과거주가를 알아보기위한 TR인 stock_mst를 요청했었습니다.
        if TRName == "stock_mst" :
            # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
            nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
            print(nCnt)

            # 받을 열만큼 가거 데이터를 받도록 합니다.
            for i in range(0, nCnt):
                # 데이터 양식
                DATA = {}

                # 데이터 받기
                DATA['ISIN_CODE'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 0)  # 표준코드
                DATA['CODE'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 1)  # 단축코드
                DATA['MARKET'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 2   )  # 장구분
                DATA['NAME'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 3)  # 종목명
                DATA['SECTOR'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 4)  # KOSPI200 세부업종
                DATA['SETTLEMENT'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 5)  # 결산연월
                DATA['SEC'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 6)  # 거래정지구분
                DATA['MANAGEMENT'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 7)  # 관리구분
                DATA['ALERT'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 8)  # 시장경보구분코드
                DATA['ROCK'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 9)  # 락구분
                DATA['INVALID'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 10)  # 불성실공시지정여부
                DATA['MARGIN'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 11)  # 증거금 구분
                DATA['CREDIT'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 12)  # 신용증거금 구분
                DATA['ETF'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 13)  # ETF 구분
                DATA['PART'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 14)  # 소속구분
                print(DATA['CODE'])

        self.rqidD.__delitem__(rqid)

    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    IndiWindow = IndiWindow()
    IndiWindow.show()
    app.exec_()