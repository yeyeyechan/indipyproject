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

class realTimeForeign(QMainWindow):

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
            ret1= self.indiReal.dynamicCall("UnRequestRTReg(QString, QString)", "SK", i['종목코드'].strip())
            if not ret1:
                print("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 해제 실패!!!")
            else:
                print("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 해제 성공!!!")
        for i in collection.find():
            ret1 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "SK", i['종목코드'].strip())
            if not ret1:
                print("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 실패!!!")
            else:
                print("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 성공!!!")

            #ret1 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "SK", i)


    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveRTData(self, realType):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        client = MongoClient('127.0.0.1', 27017)
        collection_title = "SK_" + str(datetime.today().strftime("%Y%m%d"))
        db = client[str(datetime.today().strftime("%Y%m%d"))]
        collection = db[collection_title]
        print(True)
        print(realType)
        if realType == "SK":
            DATA = {}
            # 데이터 받기
            DATA['단축코드'] = self.indiReal.dynamicCall("GetSingleData(int)", 1)
            DATA['시간'] = self.indiReal.dynamicCall("GetSingleData(int)", 2)
            DATA['외국계순매수수량'] = self.indiReal.dynamicCall("GetSingleData(int)", 47)

            print(DATA)
            print(collection.insert(DATA))

    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    realTimeForeignVar = realTimeForeign()
    app.exec_()
