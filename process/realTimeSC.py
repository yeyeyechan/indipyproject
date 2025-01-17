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

class realTimeSC(QMainWindow):

    def __init__(self):
        super().__init__()
        telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
        self.bot = telegram.Bot(token=telgm_token)
        self.processID = os.getpid()
        self.realTimeLogger = logging_instance("realTimeSC.py_ PID: "+(str)(self.processID)).mylogger
        self.realTimeLogger.info("SC 함수 실행 PID: "+(str)(self.processID))
        self.realTimeLogger.info("QAxWidget Call")
        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.realTimeLogger.info("QAxWidget Call 이후")
        self.timeline = common_min_shortTime(5).timeline
        self.date = datetime.today().strftime("%Y%m%d")
        # Indi API event
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)

        collection_name = str(datetime.today().strftime("%Y%m%d")) + "_pr_input"
        client = MongoClient('127.0.0.1', 27017)
        db = client[str(datetime.today().strftime("%Y%m%d"))]
        collection = db[collection_name]

        collection_title1 = "SC_5min_" + str(datetime.today().strftime("%Y%m%d"))
        self.collection1 = db[collection_title1]
        collection_title2 = "SC_check_" + str(datetime.today().strftime("%Y%m%d"))
        self.collection2 = db[collection_title2]

        for i in collection.find():
            ret1= self.indiReal.dynamicCall("UnRequestRTReg(QString, QString)", "SC", i['종목코드'].strip())
            self.realTimeLogger.info("ret1 " + str(ret1))
            if not ret1:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SC 실시간 등록 해제 실패!!!")
            else:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SC 실시간 등록 해제 성공!!!")
        for i in collection.find():
            ret2 = self.indiReal.dynamicCall("RequestRTReg(QString, QString)", "SC", i['종목코드'].strip())
            self.realTimeLogger.info("ret2 " + str(ret2))
            if not ret2:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SC 실시간 등록 실패!!!")
            else:
                self.realTimeLogger.info("종목코드 "+i['종목코드']+ " 에 대한 SC 실시간 등록 성공!!!")


    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveRTData(self, realType):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        self.realTimeLogger = logging_instance("SC ReceiveRTData PID: "+(str)(self.processID)).mylogger

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

            self.realTimeLogger.info(DATA)
            data_time = (int)((int)(DATA['TIME'])/10000)
            self.realTimeLogger.info("5분 간격 현물 현제가 데이터 저장 전")
            for times in self.timeline:
                if (int)(times)<data_time:
                    continue
                elif (int)(times) >= data_time:
                    DATA['TIME'] = times
                    DATA['SortTime'] = (int)(times)
                    if DATA['SortTime'] <=905:
                        if self.indiReal.dynamicCall("GetSingleData(int)", 4) == "2":
                            self.bot.sendMessage(chat_id='813531834', text="종목코드  "+  DATA['stock_code']+ "  장 시작 5분내  전일 종가 대비 상승")
                            if self.collection2.find_one({'stock_code': DATA['stock_code']}):
                                data_input = self.collection2.find_one({'stock_code': DATA['stock_code']}).copy()
                                DATA['_id'] = data_input['_id']
                                self.realTimeLogger.info(self.collection2.replace_one(data_input, DATA, upsert=True))
                            else:
                                self.realTimeLogger.info(self.collection2.insert_one(DATA))
                        else:
                            if self.collection2.find_one({'stock_code': DATA['stock_code']}):
                                self.bot.sendMessage(chat_id='813531834',text="종목코드  " + DATA['stock_code'] + "  장 시작 5분내  전일 종가 대비 하락")
                                self.collection2.delete_one({'stock_code': DATA['stock_code']})
                            else:
                                pass
                    print("DATA")
                    print(DATA)
                    if '_id' in DATA.keys():
                        print(DATA['_id'])
                        del DATA['_id']
                    self.realTimeLogger.info("self.collection1.find_one({'stock_code': DATA['stock_code'], 'TIME': times})")
                    self.realTimeLogger.info(self.collection1.find_one({'stock_code': DATA['stock_code'], 'TIME': times}))
                    self.realTimeLogger.info("self.collection1.find_one({'stock_code': DATA['stock_code'], 'TIME': times})")
                    if self.collection1.find_one({'stock_code': DATA['stock_code'], 'TIME': times}):
                        data_input = self.collection1.find_one({'stock_code': DATA['stock_code'], 'TIME': times}).copy()
                        DATA['_id'] = data_input['_id']
                        self.realTimeLogger.info(self.collection1.replace_one(data_input, DATA, upsert=True))
                        break
                    else:
                        self.realTimeLogger.info(self.collection1.insert_one(DATA))
                        break
            self.realTimeLogger.info("5분 간격 현물 현제가 데이터 저장 후")
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    realTimeSCVar = realTimeSC()
    app.exec_()
