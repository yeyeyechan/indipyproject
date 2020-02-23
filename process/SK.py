import sys

from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from pymongo import MongoClient
from datetime import datetime
from log.logger_pyflask import logging_instance
from analysis.common_data import common_min_shortTime
class SK(QMainWindow):

    def __init__(self):
        super().__init__()
        self.realTimeLogger = logging_instance("SK.py_").mylogger
        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.timeline = common_min_shortTime(5).timeline

        # Indi API event
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)

        collection_name = str(datetime.today().strftime("%Y%m%d")) + "_pr_input"
        client = MongoClient('127.0.0.1', 27017)
        db = client[str(datetime.today().strftime("%Y%m%d"))]
        collection = db[collection_name]
        for i in collection.find():
            ret1= self.indiReal.dynamicCall("UnRequestRTReg(QString, QString)", "SK", i['종목코드'].strip())
            self.realTimeLogger.info("ret1 " + ret1)
            if not ret1:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 해제 실패!!!")
            else:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 해제 성공!!!")
        for i in collection.find():
            ret1 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "SK", i['종목코드'].strip())
            self.realTimeLogger.info("ret1 " + ret1)
            if not ret1:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 실패!!!")
            else:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SK 실시간 등록 성공!!!")


    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveRTData(self, realType):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        client = MongoClient('127.0.0.1', 27017)
        collection_title1 = "SK_" + str(datetime.today().strftime("%Y%m%d"))
        collection_title2 = "SK_5min_" + str(datetime.today().strftime("%Y%m%d"))

        db = client[str(datetime.today().strftime("%Y%m%d"))]
        collection1 = db[collection_title1]
        collection2 = db[collection_title2]
        print(True)
        print(realType)
        if realType == "SK":
            DATA = {}
            # 데이터 받기
            DATA['단축코드'] = self.indiReal.dynamicCall("GetSingleData(int)", 1)
            DATA['시간'] = self.indiReal.dynamicCall("GetSingleData(int)", 2)
            DATA['외국계순매수수량'] = self.indiReal.dynamicCall("GetSingleData(int)", 47)

            self.realTimeLogger.info(DATA)
            self.realTimeLogger.info("실시간 외국인 수급 데이터 저장 전")
            self.realTimeLogger.info(collection1.insert(DATA))
            self.realTimeLogger.info("실시간 외국인 수급 데이터 저장 후")

            data_time = (int)((int)(DATA['시간'])/100)
            self.realTimeLogger.info("5분 간격 외국인 수급 데이터 저장 전")
            for times in self.timeline:
                if (int)(times)<data_time:
                    continue
                elif (int)(times) >= data_time:
                    DATA['시간'] = times
                    if self.collection2.find_one({'단축코드': DATA['단축코드'], '시간': times}):
                        self.collection2.update( self.collection2.find_one({'단축코드': DATA['단축코드'], '시간': times}), DATA, upsert=True)
                        break
                    else:
                        self.collection2.insert(DATA)
                        break
            self.realTimeLogger.info("5분 간격 외국인 수급 데이터 저장  후")
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    realTimeForeignVar = SK()
    app.exec_()
