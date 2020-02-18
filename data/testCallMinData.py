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



'''
    신한아이 인디 국내주식 실시간 거래원 데이터 조회
'''

class testCallMinData(QMainWindow):
    def __init__(self, stockCode):
        super().__init__()
        self.stockCode = stockCode

        # 실시간 TR OCX
        self.IndiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.IndiReal.ReceiveRTData.connect(self.ReceiveRTData) # 실시간 TR에 대한 응답을 받는 함수를 연결해줍니다.

        # TR ID를 저장해놓고 처리할 딕셔너리 생성
        self.rqidD = {}

        self.btn_Search  #  'btn_Search' 함수가 실행됩니다.

    # 버튼을 누르면 일반TR로 현재가 조회를 먼저 요청을 합니다.
    def btn_Search(self):
        # 조회할 종목의 이름을 받아옵니다.
        Symbol = self.stockCode
        self.MainSymbol = Symbol

        # 기존종목 실시간 TR연결 해제, 여러 종목을 실시간 TR에 등록해도 상관없습니다.
        if self.MainSymbol != "":
            self.IndiReal.dynamicCall("UnRequestRTReg(QString, QString)", "SK", self.MainSymbol)
        # 종목 현재가 조회, 일반TR로 요청합니다. 바로 실시간 TR을 등록해도 상관없습니다. 
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "SK")
        # 실시간 등록
        ret = self.IndiReal.dynamicCall("RequestRTReg(QString, QString)", "SK", self.MainSymbol)
    # 실시간 등록을 진행하고 실시간으로 데이터를 받아오도록 한다.
    def ReceiveRTData(self, RealType):

        if RealType == "SK":
            columnName = { "표준코드          "
            , "단축코드          "
            , "체결시간          "
            , "매도거래원번호    "
            , "매수거래원번호    "
            , "매도수량          "
            , "매수수량          "
            , "매도대금          "
            , "매수대금          "
            , "매도거래원번호    "
            , "매수거래원번호    "
            , "매도수량          "
            , "매수수량          "
            , "매도대금          "
            , "매수대금          "
            , "매도거래원번호    "
            , "매수거래원번호    "
            , "매도수량          "
            , "매수수량          "
            , "매도대금          "
            , "매수대금          "
            , "매도거래원번호    "
            , "매수거래원번호    "
            , "매도수량          "
            , "매수수량          "
            , "매도대금          "
            , "매수대금          "
            , "매도거래원번호    "
            , "매수거래원번호    "
            , "매도수량          "
            , "매수수량          "
            , "매도대금          "
            , "매수대금          "
            , "총매도수량        "
            , "총매수수량        "
            , "총매도대금        "
            , "총매수대금        "
            , "국내총매도수량    "
            , "국내총매수수량    "
            , "국내총매도대금    "
            , "국내총매수대금    "
            , "국내총순매수수량  "
            , "국내총순매수대금  "
            , "외국계총매도수량  "
            , "외국계총매수수량  "
            , "외국계총매도대금  "
            , "외국계총매수대금  "
            , "외국계순매수수량  "
            , "외국계순매수대금  "
            , "전체총매도수량    "
            , "전체총매수수량    "
            , "전체총매도대금    "
            , "전체총매수대금    "
            , "전체순매수수량    "
            , "전체순매수대금    "
            , "매도증가수량      "
            , "매수증가수량      "
            , "매도증가수량      "
            , "매수증가수량      "
            , "매도증가수량      "
            , "매수증가수량      "
            , "매도증가수량      "
            , "매수증가수량      "
            , "매도증가수량      "
            , "매수증가수량      "}

            DATA = {}
            DATA[columnName[0].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 0)
            DATA[columnName[1].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 1)
            DATA[columnName[2].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 2)
            DATA[columnName[3].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 3)
            DATA[columnName[4].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 4)
            DATA[columnName[5].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 5)
            DATA[columnName[6].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 6)
            DATA[columnName[7].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 7)
            DATA[columnName[8].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 8)
            DATA[columnName[9].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 9)
            DATA[columnName[10].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 10)
            DATA[columnName[11].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 11)
            DATA[columnName[12].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 12)
            DATA[columnName[13].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 13)
            DATA[columnName[14].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 14)
            DATA[columnName[15].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 15)
            DATA[columnName[16].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 16)
            DATA[columnName[17].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 17)
            DATA[columnName[18].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 18)
            DATA[columnName[19].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 19)
            DATA[columnName[20].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 20)
            DATA[columnName[21].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 21)
            DATA[columnName[22].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 22)
            DATA[columnName[23].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 23)
            DATA[columnName[24].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 24)
            DATA[columnName[25].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 25)
            DATA[columnName[26].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 26)
            DATA[columnName[27].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 27)
            DATA[columnName[28].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 28)
            DATA[columnName[29].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 29)
            DATA[columnName[30].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 30)
            DATA[columnName[31].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 31)
            DATA[columnName[32].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 32)
            DATA[columnName[33].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 33)
            DATA[columnName[34].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 34)
            DATA[columnName[35].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 35)
            DATA[columnName[36].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 36)
            DATA[columnName[37].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 37)
            DATA[columnName[38].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 38)
            DATA[columnName[39].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 39)
            DATA[columnName[40].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 40)
            DATA[columnName[41].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 41)
            DATA[columnName[42].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 42)
            DATA[columnName[43].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 43)
            DATA[columnName[44].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 44)
            DATA[columnName[45].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 45)
            DATA[columnName[46].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 46)
            DATA[columnName[47].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 47)
            DATA[columnName[48].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 48)
            DATA[columnName[49].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 49)
            DATA[columnName[50].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 50)
            DATA[columnName[51].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 51)
            DATA[columnName[52].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 52)
            DATA[columnName[53].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 53)
            DATA[columnName[54].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 54)
            DATA[columnName[55].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 55)
            DATA[columnName[56].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 56)
            DATA[columnName[57].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 57)
            DATA[columnName[58].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 58)
            DATA[columnName[59].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 59)
            DATA[columnName[60].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 60)
            DATA[columnName[61].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 61)
            DATA[columnName[62].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 62)
            DATA[columnName[63].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 63)
            DATA[columnName[64].strip()] = self.IndiReal.dynamicCall("GetSingleData(int)", 64)

            print(DATA)

    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    IndiWindow = testCallMinData("140410")
    IndiWindow.show()
    app.exec_()

