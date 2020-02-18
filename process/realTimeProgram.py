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
from datetime import datetime
from data.common import weekday_check

class realTimeProgram(QMainWindow):

    def __init__(self):
        super().__init__()


        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)

        collection_name = str(datetime.today().strftime("%Y%m%d")) + "_pr_input"
        client = MongoClient('127.0.0.1', 27017)
        db = client[str(datetime.today().strftime("%Y%m%d"))]
        collection = db[collection_name]
        for i in collection.find():
            ret1= self.indiReal.dynamicCall("UnRequestRTReg(QString, QString)", "SP", i['종목코드'].strip())
            if not ret1:
                print("종목코드 "+i['종목코드']+ " 에 대한 SP 실시간 등록 해제 실패!!!")
            else:
                print("종목코드 "+i['종목코드']+ " 에 대한 SP 실시간 등록 해제 성공!!!")
        for i in collection.find():
            ret1 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "SP", i['종목코드'].strip())
            if not ret1:
                print("종목코드 "+i['종목코드']+ " 에 대한 SP 실시간 등록 실패!!!")
            else:
                print("종목코드 "+i['종목코드']+ " 에 대한 SP 실시간 등록 성공!!!")

            #ret1 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "SK", i)


    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveRTData(self, realType):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        client = MongoClient('127.0.0.1', 27017)
        collection_title = "SP_" + str(datetime.today().strftime("%Y%m%d"))
        db = client[str(datetime.today().strftime("%Y%m%d"))]
        collection = db[collection_title]
        print(True)
        print(realType)
        if realType == "SP":
            DATA = {}
            # 데이터 받기
            DATA['단축코드'] = self.indiReal.dynamicCall("GetSingleData(int)", 1)
            DATA['일자'] = self.indiReal.dynamicCall("GetSingleData(int)", 2)
            DATA['시간'] = self.indiReal.dynamicCall("GetSingleData(int)", 3)
            DATA['매도위탁체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 12))
            DATA['매도자기체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 13))
            DATA['매수위탁체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 14))
            DATA['매수자기체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 15))
            DATA['매도위탁체결금액'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 16))
            DATA['매도자기체결금액'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 17))
            DATA['매수위탁체결금액'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 18))
            DATA['매수자기체결금액'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 19))
            DATA['차익매도위탁체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 27))
            DATA['차익매수위탁체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 28))
            DATA['차익매수자기체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 29))
            DATA['비차익매도위탁체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 30))
            DATA['비차익매도자기체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 31))
            DATA['비차익매수위탁체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 32))
            DATA['비차익매수자기체결수량'] = int(self.indiReal.dynamicCall("GetSingleData(int)", 33))
            print("realtime")
            print(DATA)
            print(collection.insert(DATA))

        '''if rqid == "SK":
            DATA = {}
            # 데이터 받기
            DATA['단축코드'] = self.IndiTR.dynamicCall("GetSingleData(int)", 1)
            DATA['체결시간'] = self.IndiTR.dynamicCall("GetSingleData(int)", 2)
            DATA['시간'] = self.IndiTR.dynamicCall("GetSingleData(int)", 3)
            DATA['국내총순매수수량'] = int(self.IndiTR.dynamicCall("GetSingleData(int)", 41))
            DATA['외국계순매수수량'] = int(self.IndiTR.dynamicCall("GetSingleData(int)", 47))
            DATA['전체순매수수량'] = int(self.IndiTR.dynamicCall("GetSingleData(int)", 53))
            print(collection.insert(DATA))'''
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    realTimeProgramVar = realTimeProgram()
    app.exec_()
