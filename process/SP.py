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
class SP(QMainWindow):

    def __init__(self):
        super().__init__()
        self.processID = os.getpid()

        self.realTimeLogger = logging_instance("SP.py_ PID: "+(str)(self.processID)).mylogger
        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)
        self.timeline = common_min_shortTime(5).timeline

        #collection_name ="20200224" + "_pr_input"
        collection_name = str(datetime.today().strftime("%Y%m%d")) + "_pr_input"
        client = MongoClient('127.0.0.1', 27017)
        #db = client["20200224"]
        db = client[str(datetime.today().strftime("%Y%m%d"))]
        collection = db[collection_name]

        collection_title1 = "SP_" + str(datetime.today().strftime("%Y%m%d"))
        collection_title2 = "SP_5min_" + str(datetime.today().strftime("%Y%m%d"))

        self.collection1 = db[collection_title1]
        self.collection2 = db[collection_title2]
        #db = client["20200222"]
        collection = db[collection_name]
        for i in collection.find():
            ret1= self.indiReal.dynamicCall("UnRequestRTReg(QString, QString)", "SP", i['종목코드'].strip())
            self.realTimeLogger.info("ret1 " + str(ret1))
            if not ret1:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SP 실시간 등록 해제 실패!!!")
            else:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SP 실시간 등록 해제 성공!!!")
        for i in collection.find():
            ret1 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "SP", i['종목코드'].strip())
            self.realTimeLogger.info("ret1 " + str(ret1))
            if not ret1:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SP 실시간 등록 실패!!!")
            else:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SP 실시간 등록 성공!!!")

    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveRTData(self, realType):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        self.realTimeLogger = logging_instance("SP ReceiveRTData PID: "+(str)(self.processID)).mylogger

        self.realTimeLogger.info(True)
        self.realTimeLogger.info(realType)
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
            self.realTimeLogger.info(DATA)
            self.realTimeLogger.info("실시간 프로그램 수급 데이터 저장 전")
            self.realTimeLogger.info(self.collection1.insert_one(DATA))
            self.realTimeLogger.info("실시간 프로그램 수급 데이터 저장 후")

            data_time = (int)((int)(DATA['시간'])/100)
            self.realTimeLogger.info("5분 간격 프로그램 수급 데이터 저장 전")
            for times in self.timeline:
                if (int)(times)<data_time:
                    continue
                elif (int)(times) >= data_time:
                    DATA['시간'] = times
                    if self.collection2.find_one({'단축코드': DATA['단축코드'], '시간': times}):
                        print(type(self.collection2.find_one({'단축코드': DATA['단축코드'], '시간': times})))
                        data_input = self.collection2.find_one({'단축코드': DATA['단축코드'], '시간': times}).copy()
                        DATA['_id']=data_input['_id']
                        self.collection2.replace_one(data_input, DATA, upsert=True)
                        break
                    else:
                        self.collection2.insert_one(DATA)
                        break
            self.realTimeLogger.info("5분 간격 프로그램 수급 데이터 저장  후")

    def ReceiveSysMsg(self, MsgID):
        self.realTimeLogger.info("System Message Received = ", MsgID)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    realTimeProgramVar = SP()
    app.exec_()
