'''
TRAM-ID : TR_SCHART
TR 내용 : 현물 분/일/주

INPUT FIELD
[Single 데이터】
Field#	항 목 명	SIZE	항 목 내 용 설 명

0	   단축코드	     6

1	   그래프종류	1	    1:분데이터 		D:일데이터
                            W:주데이터		M:월데이터

2	   시간간격	     3	    분데이터일 경우 1 – 30
                            일/주/월데이터일 경우 1

3	    시작일	     8	    YYYYMMDD
                            분 데이터 요청시 : “00000000”


4	    종료일	    8	    YYYYMMDD
                            분 데이터 요청시 : “99999999”

5	    조회갯수	    4	    1 – 9999

'''

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")

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

class TR_SCHART(QMainWindow):
    def __init__(self, stock_code, korName , standard, term, start_date, end_date, counts,date):
        super().__init__()
        self.realTimeLogger = logging_instance("TR_SCHART.py_").mylogger
        self.timeline = common_min_shortTime(5).timeline

        # 인디의 TR을 처리할 변수를 생성합니다.
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.realTimeLogger.info("start")
        self.realTimeLogger.info(counts)
        self.realTimeLogger.info(stock_code)
        self.realTimeLogger.info(korName)
        self.realTimeLogger.info(standard)
        self.realTimeLogger.info(term)
        self.realTimeLogger.info(start_date)
        self.realTimeLogger.info(end_date)
        self.realTimeLogger.info(counts)
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.korName= korName
        self.stock_code= stock_code
        self.standard= standard
        self.term= term
        self.start_date= start_date
        self.end_date= end_date
        self.counts= counts
        self.date= date

        self.client = MongoClient('127.0.0.1', 27017)
        db_name =self.date
        #test
        #db_name = "20200221"
        self.db = self.client[db_name]
        self.collection_name1 = "TR_SCHART_" + db_name
        self.collection_name2 = "TR_SCHART_5min_" + db_name

        self.collection1 = self.db [self.collection_name1]
        self.collection2 = self.db [self.collection_name2]
        self.realTimeLogger.info("start TR_SCHART")
        #self.market = market
        self.btn_Search()

    # 그럼 실제로 과거 주가를 받아오는 부분은 다음과 같습니다.
    def btn_Search(self):

        # 차트조회 : 과거주가는 차트조회를 통해 받아올 수 있습니다.
        # TR_SCHART : 과거주가를 요청할 TR입니다.
        # 해당 TR의 필드입력형식에 맞춰서 TR을 날리면 됩니다.
        # 데이터 요청 형식
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "TR_SCHART")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.stock_code) # 단축코드
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1, self.standard) # 1:분봉, D:일봉, W:주봉, M:월봉
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2,   self.term) # 분봉: 1~30, 일/주/월 : 1
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3, self.start_date) # 시작일(YYYYMMDD)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 4, self.end_date) # 종료일(YYYYMMDD)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 5, self.counts) # 조회갯수(1~9999)
        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청
        print("btn_search")
    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        print("receive Data")
        self.realTimeLogger = logging_instance("TR_SCHART.py_receive Data_").mylogger

        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        print(nCnt)

        # 받을 열만큼 가거 데이터를 받도록 합니다.
        for i in range(0, nCnt):
            # 데이터 양식
            DATA = {}

            # 데이터 받기
            DATA['DATE'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 0)  # 일자
            DATA['TIME'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 1)  # 시간
            DATA['OPEN'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 2)  # 시가
            DATA['HIGH'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 3)  # 고가
            DATA['Low'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 4)  # 저가
            DATA['Close'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 5)  # 종가
            DATA['Price_ADJ'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 6)  # 주가수정계수
            DATA['Vol_ADJ'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 7)  # 거래량 수정계수
            DATA['Rock'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 8)  # 락구분
            DATA['Vol'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 9)  # 단위거래량
            DATA['Trading_Value'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 10)  # 단위거래대금

            DATA['stock_code'] = self.stock_code # 주식코드
            DATA['korName'] = self.korName.strip() # 한글 이름
            #DATA['start_date'] = self.start_date # 시작일
            #DATA['end_date'] = self.end_date  # 마지막일
            #DATA['market'] = self.market # market




            self.realTimeLogger.info(DATA)
            self.realTimeLogger.info("실시간 현재가 데이터 저장 전")
            if self.collection1.find_one({'stock_code':  self.stock_code, 'TIME':  DATA['TIME'] }):
                self.collection1.update(self.collection1.find_one({'stock_code':  self.stock_code, 'TIME':  DATA['TIME'] }), DATA, upsert=True)
            else:
                self.collection1.insert(DATA)
            self.realTimeLogger.info("실시간 현재가  데이터 저장 후")

            data_time = (int)(DATA['TIME'])
            self.realTimeLogger.info("5분 간격 현재가 데이터 저장 전")
            for times in self.timeline:
                if (int)(times) < data_time:
                    continue
                elif (int)(times) >= data_time:
                    DATA['TIME'] = times
                    if self.collection2.find_one({'stock_code': DATA['stock_code'], 'TIME': times}):
                        self.collection2.update(self.collection2.find_one({'stock_code': DATA['stock_code'], 'TIME': times}), DATA,upsert=True)
                        break
                    else:
                        self.collection2.insert(DATA)
                        break
            self.realTimeLogger.info("5분 간격현재가 데이터 저장  후")
        QCoreApplication.instance().exit(0)

    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
def TR_SCHART_function():
    realTimeLogger = logging_instance("TR_SCHART_function.py_").mylogger
    try:
        py_day = datetime.datetime.today().strftime("%Y%m%d")
        date = str(datetime.datetime.today().strftime("%Y%m%d"))
        #test
        #date = "20200221"
        py_time = datetime.datetime.now()
        hour = py_time.hour
        min = py_time.minute
        if (hour == 15 and min >= 30) or  hour > 15:
            hour = 15
            min = 30
        if py_day != date:
            hour = 15
            min = 30
        #78개임(날) 905-1530
        total_time = (int)((hour*60+min - 9*60 -5)/5)
        if total_time <=-1:
            realTimeLogger.info("5분 간격현재가 데이터 저장  가능 시간 아님")
        elif total_time >-1 and total_time<=0:
            total_time =1
        elif total_time==77:
            total_time +=1
        else:
            total_time +=2

        client = MongoClient('127.0.0.1', 27017)
        db = client[date]

        collection_name = date+"_pr_input"
        collection1 = db[collection_name]

        total_len = collection1.count()
        checkIndex = 0
        realTimePriceEvent = QApplication(sys.argv)

        short_time = common_min_shortTime(5)
        realTimeLogger.info("현재 가장 마지막으로 기록될 현재가 시간은   "+ str(hour)+":"+str(min))
        realTimeLogger.info("종목의 총 갯수 는 "+ str(total_len))
        realTimeLogger.info("각종목별 총 기록될 현재가 갯수는 (5분기준 현시각 라스트)     "+str(total_time))
        for i in collection1.find():
            realTimeLogger.info(i['종목코드'])
            TR_SCHART_vari = TR_SCHART(i['종목코드'], i['korName'].strip(), '1', '5', "00000000", "99999999",str(total_time),date)
            time.sleep(0.3)
            checkIndex +=1
        if checkIndex != total_len+1:
            realTimePriceEvent.exec()
            print("ssibal")
        realTimeLogger.info("지금은 현재가 데이터 저장 성공")
    except Exception:
        realTimeLogger.info("지금은 현재가 데이터 저장 실패")
if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.add_job(TR_SCHART_function, 'cron', hour ='0',minute= '*/1',second='1')
    sched.start()

