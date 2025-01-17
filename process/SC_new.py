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
from analysis.common_data import common_min_shortTime, make_five_min
import telegram

class SC_new(QMainWindow):

    def __init__(self):
        super().__init__()

        telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
        self.bot = telegram.Bot(token=telgm_token)
        self.processID = os.getpid()
        self.realTimeLogger = logging_instance("SC_new.py_ PID: "+(str)(self.processID)).mylogger
        self.realTimeLogger.info("SC_new 함수 실행 PID: "+(str)(self.processID))
        self.realTimeLogger.info("QAxWidget Call")
        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.realTimeLogger.info("QAxWidget Call 이후")
        # 0905 시간 배열
        self.timeline = common_min_shortTime(5).timeline
        #오늘 날짜
        self.db_date = datetime.today().strftime("%Y%m%d")
        # Indi API event
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)

        collection_name = self.db_date+ "_pr_input"
        client = MongoClient('127.0.0.1', 27017)
        db = client[self.db_date]
        #모니터링 대상 종목 컬렉션
        self.monitoring_input_collection = db[collection_name]
        #모니터링 대상 종목 현재가 데이터 컬랙션
        collection_title1 = "SC_5min_" + self.db_date
        self.SC_5min = db[collection_title1]
        #모니터링 중 선정된 종목 여부 컬렉션
        collection_title2 = "SC_check_" + self.db_date
        self.SC_check = db[collection_title2]

        for i in self.monitoring_input_collection.find():
            ret1= self.indiReal.dynamicCall("UnRequestRTReg(QString, QString)", "SC", i['단축코드'].strip())
            self.realTimeLogger.info("ret1 " + str(ret1))
            if not ret1:
                self.realTimeLogger.info("단축코드 "+i['단축코드']+ " 에 대한 SC 실시간 등록 해제 실패!!!")
            else:
                self.realTimeLogger.info("단축코드 "+i['단축코드']+ " 에 대한 SC 실시간 등록 해제 성공!!!")
        for i in self.monitoring_input_collection.find():
            ret2 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "SC", i['단축코드'].strip())
            self.realTimeLogger.info("ret2 " + str(ret2))
            if not ret2:
                self.realTimeLogger.info("단축코드 "+i['단축코드']+ " 에 대한 SC 실시간 등록 실패!!!")
            else:
                self.realTimeLogger.info("단축코드 "+i['단축코드']+ " 에 대한 SC 실시간 등록 성공!!!")
    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveRTData(self, realType):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        self.realTimeLogger = logging_instance("SC_new.py 데이터 전송 받음 PID: "+(str)(self.processID)).mylogger
        if realType == "SC":
            DATA = {}
            # 데이터 받기
            DATA['DATE'] = self.db_date
            DATA['TIME'] = self.indiReal.dynamicCall("GetSingleData(int)", 2) #1630 0000
            DATA['OPEN'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 10))
            DATA['HIGH'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 11))
            DATA['LOW'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 12))
            DATA['Close'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 3))
            DATA['Vol'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 7))
            DATA['Trading_Value'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 8))
            DATA['stock_code'] = self.indiReal.dynamicCall("GetSingleData(int)", 1)
            DATA['단축코드'] = self.indiReal.dynamicCall("GetSingleData(int)", 1)
            self.realTimeLogger.info("SC_new 전송 받은 데이터 :")
            self.realTimeLogger.info(DATA)
            DATA['sortTime'] = make_five_min(DATA['TIME'])
            DATA['sortTimeInt'] = (int)(make_five_min(DATA['TIME']))
            if self.monitoring_input_collection.find_one({"단축코드":  DATA['단축코드']}) != None:
                if self.monitoring_input_collection.find_one({"단축코드":  DATA['단축코드']})['로직구분']  != "":
                    DATA['로직구분'] =  self.monitoring_input_collection.find_one({"단축코드":  DATA['단축코드']})['로직구분']
                else:
                    DATA['로직구분'] = "없음"
            else:
                DATA['로직구분'] = "없음"
            if (int)(DATA['sortTime']) <= 1000:
                SC_check_data= {}
                SC_check_data['stock_code'] = DATA['stock_code']
                SC_check_data['단축코드'] = DATA['stock_code']
                SC_check_data['gubun'] = self.indiReal.dynamicCall("GetSingleData(int)", 4)
                SC_check_data['당일구분'] = self.indiReal.dynamicCall("GetSingleData(int)", 4)
                if self.SC_check.find_one({'stock_code': DATA['stock_code']}):
                    data_input = self.SC_check.find_one({'stock_code': DATA['stock_code']}).copy()
                    SC_check_data['_id'] = data_input['_id']
                    self.SC_check.replace_one(data_input, SC_check_data, upsert=True)
                    self.realTimeLogger.info("장 시작 후 60분 내 상승 종목 코드 :  " + DATA['stock_code'])
                    if SC_check_data['gubun'] == "2":
                        self.realTimeLogger.info("장 시작 후 60분 내 상승 종목 코드 :  " + DATA['stock_code'])
                else:
                    self.SC_check.insert_one(SC_check_data)
                    if SC_check_data['gubun'] == "2":
                        self.realTimeLogger.info("장 시작 후 5분 내 상승 종목 코드 :  " + DATA['stock_code'])
            if  self.SC_5min.find_one({'stock_code': DATA['stock_code'], 'sortTime':  DATA['sortTime']}):
                data_input = self.SC_5min.find_one({'stock_code': DATA['stock_code'] , 'sortTime':  DATA['sortTime']}).copy()
                DATA['_id'] = data_input['_id']
                self.realTimeLogger.info("SC_new 전송 받은 데이터 시간 "+DATA['sortTime'] +" 새 데이터로 교체")
                self.realTimeLogger.info(self.SC_5min.replace_one(data_input, DATA, upsert=True))
            else:
                self.realTimeLogger.info("SC_new 전송 받은 데이터 시간 "+DATA['sortTime'] +" 새 데이터 입력")
                self.realTimeLogger.info(self.SC_5min.insert_one(DATA))
            self.realTimeLogger.info("SC_new 전송 받기 완료 종목코드 : "+ DATA['stock_code'] +" 데이터 시간 : "+DATA['sortTime'])

    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    realTimeSCVar = SC_new()
    app.exec_()
