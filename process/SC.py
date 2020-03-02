'''
TRAM-ID : SC


'''

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")
import telegram

from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
import time
from pymongo import MongoClient
from log.logger_pyflask import logging_instance
from analysis.common_data import common_min_shortTime
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

class SC(QMainWindow):
    def __init__(self, stock_code, korName, date):
        super().__init__()
        self.realTimeLogger = logging_instance("SC.py_").mylogger
        self.timeline = common_min_shortTime(5).timeline
        telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
        self.bot = telegram.Bot(token=telgm_token)

        # 인디의 TR을 처리할 변수를 생성합니다.
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.realTimeLogger.info("start")
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.stock_code= stock_code
        self.date= date
        self.korName= korName

        self.client = MongoClient('127.0.0.1', 27017)
        db_name =self.date
        self.db = self.client[db_name]
        self.collection_name1 = "SC_" + db_name

        self.collection1 = self.db [self.collection_name1]

        self.realTimeLogger.info("start SC")
        self.btn_Search()

    # 그럼 실제로 과거 주가를 받아오는 부분은 다음과 같습니다.
    def btn_Search(self):

        # 차트조회 : 과거주가는 차트조회를 통해 받아올 수 있습니다.
        # TR_SCHART : 과거주가를 요청할 TR입니다.
        # 해당 TR의 필드입력형식에 맞춰서 TR을 날리면 됩니다.
        # 데이터 요청 형식
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "SC")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.stock_code) # 단축코드
        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청
    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        self.realTimeLogger = logging_instance("SC.py_receive Data_").mylogger
        # 데이터 양식
        DATA = {}
        # 데이터 받기
        DATA['stock_code'] = self.IndiTR.dynamicCall("GetSingleData(int)", 1)  # 단축코드
        DATA['TIME'] = self.IndiTR.dynamicCall("GetSingleData(int)", 2)  # 체결시간
        DATA['GUBUN'] = self.IndiTR.dynamicCall("GetSingleData(int)", 4)  # 전일대비구분
        DATA['PRICE'] = self.IndiTR.dynamicCall("GetSingleData(int)", 3)  # 현재가
        DATA['Trading_Value'] = (int)(self.IndiTR.dynamicCall("GetSingleData(int)", 8))  # 누적거래대금
        DATA['korName'] = self.korName


        py_time = datetime.datetime.now()
        hour = py_time.hour
        min = py_time.minute
        if hour ==9 and min >=5 and  DATA['Trading_Value']  >= 100000000:
            self.bot.sendMessage(chat_id='813531834', text="종목명 : "+ DATA['stock_code'] + "   첫 5분 거래대금 1억 돌파   " +DATA['Trading_Value'])
        elif DATA['Trading_Value']  >= 2000000000:
            self.bot.sendMessage(chat_id='813531834', text="종목명 : "+ DATA['stock_code'] + "   거래대금 20억 돌파   " +DATA['Trading_Value'])

        self.realTimeLogger.info(DATA)
        self.realTimeLogger.info("5분 간격 누적거래대금 데이터 저장 전")
        if self.collection1.find_one({'stock_code': DATA['stock_code']}):
            data_input = self.collection1.find_one({'stock_code': DATA['stock_code']}).copy()
            DATA['_id'] = data_input['_id']
            if data_input['Trading_Value']*10 < DATA['Trading_Value']:
                self.bot.sendMessage(chat_id='813531834', text="종목명 : " + DATA['stock_code'] + "   거래대금 10배터짐   " )
            elif data_input['Trading_Value']*5 < DATA['Trading_Value']:
                self.bot.sendMessage(chat_id='813531834', text="종목명 : " + DATA['stock_code'] + "   거래대금 5배터짐   " )
            elif data_input['Trading_Value'] * 3 < DATA['Trading_Value']:
                self.bot.sendMessage(chat_id='813531834', text="종목명 : " + DATA['stock_code'] + "   거래대금 3배터짐   ")
            elif data_input['Trading_Value'] * 2 < DATA['Trading_Value']:
                self.bot.sendMessage(chat_id='813531834', text="종목명 : " + DATA['stock_code'] + "   거래대금 2배터짐   ")
            self.collection1.replace_one(data_input, DATA, upsert=True)
        else:
            self.collection1.insert_one(DATA)

        self.realTimeLogger.info("5분 간격 누적거래대금 데이터 저장  후")
        QCoreApplication.instance().exit(0)
    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
def SC_function():
    try:
        realTimeLogger = logging_instance("SC_function.py_").mylogger
        py_day = datetime.datetime.today().strftime("%Y%m%d")
        date = str(datetime.datetime.today().strftime("%Y%m%d"))
        #date="20200221"
        py_time = datetime.datetime.now()
        hour = py_time.hour
        min = py_time.minute

        client = MongoClient('127.0.0.1', 27017)
        db = client[date]
        collection_name = date+"_pr_input"
        collection1 = db[collection_name]
        total_len = collection1.count()
        checkIndex = 0
        realTimePriceEvent = QApplication(sys.argv)
        realTimeLogger.info("현재 가장 마지막으로 기록될 SC 시간은   "+ str(hour)+":"+str(min))
        realTimeLogger.info("종목의 총 갯수 는 "+ str(total_len))
        for i in collection1.find():
            realTimeLogger.info(i['종목코드'])
            SC_vari = SC(i['종목코드'], i['korName'].strip(),date)
            time.sleep(0.3)
            checkIndex +=1
        if checkIndex != total_len+1:
            realTimePriceEvent.exec()
    except Exception:
        realTimeLogger.info("지금은 SC 데이터 저장 실패")
    realTimeLogger.info("지금은 현재가 SC 저장 성공")
if __name__ == "__main__":
    sched_sc = BlockingScheduler()
    sched_sc.add_job(SC_function, 'cron', hour ='9-15',minute= '*/5',second='5')
    sched_sc.start()

