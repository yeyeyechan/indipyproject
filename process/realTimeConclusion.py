import sys
import os
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")

from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow


from pymongo import MongoClient
from datetime import datetime
import telegram
from log.logger_pyflask import logging_instance

#chat id 813531834
class realTimeConclusion(QMainWindow):

    def __init__(self):
        super().__init__()
        self.processID = os.getpid()

        telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
        self.bot = telegram.Bot(token=telgm_token)
        self.realTimeLogger = logging_instance("realTimeConclusion.py 실시간 체결 확인 PID: "+(str)(self.processID)).mylogger
        self.realTimeLogger.info("realTimeConclusion  OCX call")
        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)

        db_name = str(datetime.today().strftime("%Y%m%d"))
        client = MongoClient('127.0.0.1', 27017)
        self.db = client[db_name]
        self.collection_name = "AA"+db_name
        self.collection = self.db[self.collection_name]
        self.realTimeLogger.info("realTimeConclusion  AA call")

        ret1 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "AA", '*')
        if ret1 :
            print("AA 등록성공")

        if not ret1:
            print("AA 등록실패")
        self.realTimeLogger.info("realTimeConclusion  AA call 완료")

    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveRTData(self, realType):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        self.realTimeLogger = logging_instance("AA ReceiveRTData 실시간 체결 확인 PID: "+(str)(self.processID)).mylogger

        DATA = {}
        # 데이터 받기
        DATA['처리구분'] = self.indiReal.dynamicCall("GetSingleData(int)", 0)
        DATA['매수매도구분'] = self.indiReal.dynamicCall("GetSingleData(int)", 8)
        DATA['상태'] = self.indiReal.dynamicCall("GetSingleData(int)", 10)
        DATA['종목코드'] = self.indiReal.dynamicCall("GetSingleData(int)", 11)
        DATA['종목명'] = self.indiReal.dynamicCall("GetSingleData(int)", 12)
        DATA['주문수량'] = self.indiReal.dynamicCall("GetSingleData(int)", 14)
        DATA['주문가격'] = self.indiReal.dynamicCall("GetSingleData(int)", 15)
        DATA['미체결수량'] = self.indiReal.dynamicCall("GetSingleData(int)", 20)
        DATA['체결수량'] = self.indiReal.dynamicCall("GetSingleData(int)", 23)
        DATA['체결단가'] = self.indiReal.dynamicCall("GetSingleData(int)", 24)
        DATA['체결시간'] = self.indiReal.dynamicCall("GetSingleData(int)", 25)

        if DATA['매수매도구분'] == "01":
            gubun = " 매도   "
        if DATA['매수매도구분'] == "02":
            gubun = " 매수    "

        if DATA['처리구분'] == "00":
            DATA['상태메세지'] =  "종목명:  "+DATA['종목명'] +"  주문가격: "+DATA['주문가격']  +"  주문수량: "+  DATA['주문수량']  + gubun + "정상 주문 됨"
        elif DATA['처리구분'] == "03":
            DATA['상태메세지'] =  "종목명:  "+DATA['종목명'] +"  체결단가: "+DATA['체결단가']  +"  체결수량: "+  DATA['체결수량']  + gubun + "체결 됨" + "  미체결 수량 :   "+ DATA['미체결수량']
        else:
            DATA['상태메세지'] = "작업필요"
        self.realTimeLogger.info(DATA['상태메세지'])
        self.bot.sendMessage(chat_id='813531834', text=DATA['상태메세지'])
        self.collection.insert(DATA)

    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    realTimeConclusion_test = realTimeConclusion()
    app.exec_()
