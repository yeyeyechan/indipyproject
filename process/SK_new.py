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
class SK_new(QMainWindow):

    def __init__(self):
        super().__init__()
        self.processID = os.getpid()
        telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
        self.bot = telegram.Bot(token=telgm_token)
        self.realTimeLogger = logging_instance("SK_new.py_ PID: "+(str)(self.processID)).mylogger
        self.realTimeLogger.info("SK_new 클래스 실행")
        self.realTimeLogger.info("QAxWidget Call")
        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.realTimeLogger.info("QAxWidget Call 이후")
        self.timeline = common_min_shortTime(5).timeline

        # Indi API event
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)

        collection_name = str(datetime.today().strftime("%Y%m%d")) + "_pr_input"
        client = MongoClient('127.0.0.1', 27017)
        db = client[str(datetime.today().strftime("%Y%m%d"))]
        collection = db[collection_name]

        collection_title1 = "SK_" + str(datetime.today().strftime("%Y%m%d"))
        collection_title2 = "SK_5min_" + str(datetime.today().strftime("%Y%m%d"))

        self.SK = db[collection_title1]
        self.SK_5min = db[collection_title2]

        for i in collection.find():
            ret1= self.indiReal.dynamicCall("UnRequestRTReg(QString, QString)", "SK", i['종목코드'].strip())
            self.realTimeLogger.info("ret1 " + str(ret1))
            if not ret1:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 해제 실패!!!")
            else:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 해제 성공!!!")
        for i in collection.find():
            ret1 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "SK", i['종목코드'].strip())
            self.realTimeLogger.info("ret1 " + str(ret1))
            if not ret1:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 실패!!!")
            else:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 성공!!!")


    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveRTData(self, realType):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        self.realTimeLogger = logging_instance("SK_new 데이터 받기 PID: "+(str)(self.processID)).mylogger

        if realType == "SK":
            DATA = {}
            # 데이터 받기
            DATA['단축코드'] = self.indiReal.dynamicCall("GetSingleData(int)", 1)
            DATA['시간'] = self.indiReal.dynamicCall("GetSingleData(int)", 2)
            DATA['외국계순매수수량'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 47))


            self.realTimeLogger.info("실시간 외국인 수급 데이터 종목코드  "+DATA['단축코드'] )
            self.realTimeLogger.info(DATA)
            self.realTimeLogger.info("실시간 외국인 수급 데이터 저장 전 종목코드  "+DATA['단축코드'] )
            self.realTimeLogger.info(self.SK.insert_one(DATA))
            self.realTimeLogger.info("실시간 외국인 수급 데이터 저장 후 종목코드  "+DATA['단축코드'] )

            data_time = make_five_min(DATA['시간'])
            self.realTimeLogger.info("5분 간격 외국인 수급 데이터 저장 전")
            if self.SK_5min.find_one({'단축코드': DATA['단축코드'], '시간':data_time}):
                data_input = self.SK_5min.find_one({'단축코드': DATA['단축코드'], '시간':data_time}).copy()
                DATA['_id'] = data_input['_id']
                self.SK_5min.replace_one(data_input, DATA, upsert=True)
                self.realTimeLogger.info("SK_new 전송 받은 데이터 시간 "+data_time +" 새 데이터로 교체 종목코드  "+DATA['단축코드'] )
            else:
                self.SK_5min.insert_one(DATA)
                self.realTimeLogger.info("SK_new 전송 받은 데이터 시간 "+data_time +" 새 데이터로 입력 종목코드  "+DATA['단축코드'] )
            self.realTimeLogger.info("5분 간격 외국인 수급 데이터 저장  후")
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    realTimeForeignVar = SK_new()
    app.exec_()
