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
from log.logger_pyflask import logging_instance
from analysis.common_data import common_min_shortTime
import telegram

class SC_new(QMainWindow):

    def __init__(self, date):
        super().__init__()

        telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
        self.bot = telegram.Bot(token=telgm_token)
        self.processID = os.getpid()
        self.realTimeLogger = logging_instance("SC_new.py_ PID: "+(str)(self.processID)).mylogger
        self.realTimeLogger.info("SC 함수 실행 PID: "+(str)(self.processID))
        self.realTimeLogger.info("QAxWidget Call")
        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.realTimeLogger.info("QAxWidget Call 이후")
        #db 날짜
        self.db_date = date
        # 0905 시간 배열
        self.timeline = common_min_shortTime(5).timeline
        #오늘 날짜
        self.date = datetime.today().strftime("%Y%m%d")
        # Indi API event
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)

        collection_name = self.db_date+ "_pr_input"
        client = MongoClient('127.0.0.1', 27017)
        db = client[self.db_date]
        #모니터링 대상 종목 컬렉션
        monitoring_input_collection = db[collection_name]
        #모니터링 대상 종목 현재가 데이터 컬랙션
        collection_title1 = "SC_5min_" + self.db_date
        self.collection1 = db[collection_title1]
        #모니터링 중 선정된 종목 여부 컬렉션
        collection_title2 = "SC_check_" + self.db_date
        self.collection2 = db[collection_title2]

        for i in monitoring_input_collection.find():
            ret1= self.indiReal.dynamicCall("UnRequestRTReg(QString, QString)", "SC", i['종목코드'].strip())
            self.realTimeLogger.info("ret1 " + str(ret1))
            if not ret1:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SC 실시간 등록 해제 실패!!!")
            else:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SC 실시간 등록 해제 성공!!!")
        for i in monitoring_input_collection.find():
            ret2 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "SC", i['종목코드'].strip())
            self.realTimeLogger.info("ret2 " + str(ret2))
            if not ret2:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SC 실시간 등록 실패!!!")
            else:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SC 실시간 등록 성공!!!")


    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveRTData(self, realType):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        self.realTimeLogger = logging_instance("SC_new.py 데이터 전송 받음 PID: "+(str)(self.processID)).mylogger

        if realType == "SC":
            DATA = {}
            # 데이터 받기
            DATA['DATE'] = self.date
            DATA['TIME'] = self.indiReal.dynamicCall("GetSingleData(int)", 2) #1630 0000
            DATA['OPEN'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 10))
            DATA['HIGH'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 11))
            DATA['LOW'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 12))
            DATA['Close'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 3))
            DATA['Vol'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 7))
            DATA['Trading_Value'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 8))
            DATA['stock_code'] = self.indiReal.dynamicCall("GetSingleData(int)", 1)
            self.realTimeLogger.info("SC_new 전송 받은 데이터 :")
            self.realTimeLogger.info(DATA)

            hour = datetime.now().hour
            min  = datetime.now().minute

            time = hour*100+min
            data_time = (int)((int)(DATA['TIME'])/10000)


            self.realTimeLogger.info("")

    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    realTimeSCVar = SC_new()
    app.exec_()
