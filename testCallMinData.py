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

        # 일반 TR OCX
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg) # 일반 TR에 대한 응답을 받는 함수를 연결해 줍니다.

        # 실시간 TR OCX
        self.IndiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.IndiReal.ReceiveRTData.connect(self.ReceiveRTData) # 실시간 TR에 대한 응답을 받는 함수를 연결해줍니다.

        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "SK")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.stockCode) # 인풋 : 단축코드
        rqid = self.IndiTR.dynamicCall("RequestData()")
        print(rqid)
        self.columnName = {"표준코드          "
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

    # 버튼을 누르면 일반TR로 현재가 조회를 먼저 요청을 합니다.
    def ReceiveData(self, rqid):
        DATA = {}
        DATA[self.columnName[0].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 0)
        DATA[self.columnName[1].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 1)
        DATA[self.columnName[2].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 2)
        DATA[self.columnName[3].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 3)
        DATA[self.columnName[4].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 4)
        DATA[self.columnName[5].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 5)
        DATA[self.columnName[6].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 6)
        DATA[self.columnName[7].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 7)
        DATA[self.columnName[8].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 8)
        DATA[self.columnName[9].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 9)
        DATA[self.columnName[10].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 10)
        DATA[self.columnName[11].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 11)
        DATA[self.columnName[12].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 12)
        DATA[self.columnName[13].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 13)
        DATA[self.columnName[14].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 14)
        DATA[self.columnName[15].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 15)
        DATA[self.columnName[16].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 16)
        DATA[self.columnName[17].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 17)
        DATA[self.columnName[18].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 18)
        DATA[self.columnName[19].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 19)
        DATA[self.columnName[20].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 20)
        DATA[self.columnName[21].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 21)
        DATA[self.columnName[22].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 22)
        DATA[self.columnName[23].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 23)
        DATA[self.columnName[24].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 24)
        DATA[self.columnName[25].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 25)
        DATA[self.columnName[26].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 26)
        DATA[self.columnName[27].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 27)
        DATA[self.columnName[28].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 28)
        DATA[self.columnName[29].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 29)
        DATA[self.columnName[30].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 30)
        DATA[self.columnName[31].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 31)
        DATA[self.columnName[32].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 32)
        DATA[self.columnName[33].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 33)
        DATA[self.columnName[34].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 34)
        DATA[self.columnName[35].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 35)
        DATA[self.columnName[36].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 36)
        DATA[self.columnName[37].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 37)
        DATA[self.columnName[38].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 38)
        DATA[self.columnName[39].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 39)
        DATA[self.columnName[40].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 40)
        DATA[self.columnName[41].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 41)
        DATA[self.columnName[42].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 42)
        DATA[self.columnName[43].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 43)
        DATA[self.columnName[44].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 44)
        DATA[self.columnName[45].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 45)
        DATA[self.columnName[46].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 46)
        DATA[self.columnName[47].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 47)
        DATA[self.columnName[48].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 48)
        DATA[self.columnName[49].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 49)
        DATA[self.columnName[50].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 50)
        DATA[self.columnName[51].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 51)
        DATA[self.columnName[52].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 52)
        DATA[self.columnName[53].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 53)
        DATA[self.columnName[54].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 54)
        DATA[self.columnName[55].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 55)
        DATA[self.columnName[56].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 56)
        DATA[self.columnName[57].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 57)
        DATA[self.columnName[58].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 58)
        DATA[self.columnName[59].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 59)
        DATA[self.columnName[60].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 60)
        DATA[self.columnName[61].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 61)
        DATA[self.columnName[62].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 62)
        DATA[self.columnName[63].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 63)
        DATA[self.columnName[64].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 64)

        print(DATA)
        ret = self.IndiReal.dynamicCall("RequestRTReg(QString, QString)", "SK", self.stockCode)

    def ReceiveRTData(self, RealType):
        DATA = {}
        DATA[self.columnName[0].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 0)
        DATA[self.columnName[1].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 1)
        DATA[self.columnName[2].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 2)
        DATA[self.columnName[3].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 3)
        DATA[self.columnName[4].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 4)
        DATA[self.columnName[5].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 5)
        DATA[self.columnName[6].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 6)
        DATA[self.columnName[7].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 7)
        DATA[self.columnName[8].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 8)
        DATA[self.columnName[9].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 9)
        DATA[self.columnName[10].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 10)
        DATA[self.columnName[11].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 11)
        DATA[self.columnName[12].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 12)
        DATA[self.columnName[13].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 13)
        DATA[self.columnName[14].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 14)
        DATA[self.columnName[15].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 15)
        DATA[self.columnName[16].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 16)
        DATA[self.columnName[17].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 17)
        DATA[self.columnName[18].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 18)
        DATA[self.columnName[19].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 19)
        DATA[self.columnName[20].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 20)
        DATA[self.columnName[21].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 21)
        DATA[self.columnName[22].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 22)
        DATA[self.columnName[23].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 23)
        DATA[self.columnName[24].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 24)
        DATA[self.columnName[25].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 25)
        DATA[self.columnName[26].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 26)
        DATA[self.columnName[27].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 27)
        DATA[self.columnName[28].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 28)
        DATA[self.columnName[29].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 29)
        DATA[self.columnName[30].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 30)
        DATA[self.columnName[31].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 31)
        DATA[self.columnName[32].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 32)
        DATA[self.columnName[33].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 33)
        DATA[self.columnName[34].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 34)
        DATA[self.columnName[35].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 35)
        DATA[self.columnName[36].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 36)
        DATA[self.columnName[37].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 37)
        DATA[self.columnName[38].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 38)
        DATA[self.columnName[39].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 39)
        DATA[self.columnName[40].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 40)
        DATA[self.columnName[41].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 41)
        DATA[self.columnName[42].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 42)
        DATA[self.columnName[43].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 43)
        DATA[self.columnName[44].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 44)
        DATA[self.columnName[45].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 45)
        DATA[self.columnName[46].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 46)
        DATA[self.columnName[47].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 47)
        DATA[self.columnName[48].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 48)
        DATA[self.columnName[49].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 49)
        DATA[self.columnName[50].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 50)
        DATA[self.columnName[51].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 51)
        DATA[self.columnName[52].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 52)
        DATA[self.columnName[53].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 53)
        DATA[self.columnName[54].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 54)
        DATA[self.columnName[55].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 55)
        DATA[self.columnName[56].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 56)
        DATA[self.columnName[57].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 57)
        DATA[self.columnName[58].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 58)
        DATA[self.columnName[59].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 59)
        DATA[self.columnName[60].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 60)
        DATA[self.columnName[61].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 61)
        DATA[self.columnName[62].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 62)
        DATA[self.columnName[63].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 63)
        DATA[self.columnName[64].strip()] = self.IndiTR.dynamicCall("GetSingleData(int)", 64)

        print(DATA)

    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    IndiWindow = testCallMinData("140410") #메지온
    app.exec_()

