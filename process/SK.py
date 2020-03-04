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
class SK(QMainWindow):

    def __init__(self):
        super().__init__()
        self.processID = os.getpid()
        telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
        self.bot = telegram.Bot(token=telgm_token)
        self.realTimeLogger = logging_instance("SK.py_ PID: "+(str)(self.processID)).mylogger
        self.realTimeLogger.info("SK 함수 실행")
        self.realTimeLogger.info("QAxWidget Call")
        self.indiReal = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.realTimeLogger.info("QAxWidget Call 이후")
        self.timeline = common_min_shortTime(5).timeline

        # Indi API event
        self.indiReal.ReceiveRTData.connect(self.ReceiveRTData)

        collection_name = str(datetime.today().strftime("%Y%m%d")) + "_pr_input"
        #collection_name = "20200228" + "_pr_input"
        client = MongoClient('127.0.0.1', 27017)
        db = client[str(datetime.today().strftime("%Y%m%d"))]
        #db = client["20200228"]
        collection = db[collection_name]

        collection_title1 = "SK_" + str(datetime.today().strftime("%Y%m%d"))
        collection_title2 = "SK_5min_" + str(datetime.today().strftime("%Y%m%d"))

        collection_title3 = "SC_check_" + str(datetime.today().strftime("%Y%m%d"))
        self.collection3 = db[collection_title3]

        collection_title4 = "SK_check_" + str(datetime.today().strftime("%Y%m%d"))
        self.collection4 = db[collection_title4]

        collection_title5 = "TR_1206_new_2"
        self.collection5 = db[collection_title5]
        #db = client[str(datetime.today().strftime("%Y%m%d"))]
        self.collection1 = db[collection_title1]
        self.collection2 = db[collection_title2]
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
        self.realTimeLogger = logging_instance("SK ReceiveRTData PID: "+(str)(self.processID)).mylogger

        print(True)
        print(realType)
        if realType == "SK":
            DATA = {}
            # 데이터 받기
            DATA['단축코드'] = self.indiReal.dynamicCall("GetSingleData(int)", 1)
            DATA['시간'] = self.indiReal.dynamicCall("GetSingleData(int)", 2)
            DATA['외국계순매수수량'] = (int)(self.indiReal.dynamicCall("GetSingleData(int)", 47))

            self.realTimeLogger.info(DATA)
            self.realTimeLogger.info("실시간 외국인 수급 데이터 저장 전")
            self.realTimeLogger.info(self.collection1.insert_one(DATA))
            self.realTimeLogger.info("실시간 외국인 수급 데이터 저장 후")

            data_time = (int)((int)(DATA['시간'])/100)
            self.realTimeLogger.info("5분 간격 외국인 수급 데이터 저장 전")
            for times in self.timeline:
                if (int)(times)<data_time:
                    continue
                elif (int)(times) >= data_time:
                    DATA['시간'] = times
                    if self.collection3.find_one({'stock_code': DATA['단축코드']}):
                        vol =  self.collection3.find_one({'stock_code': DATA['단축코드']})['Vol']
                        current_foreign_ratio = (int)(DATA['외국계순매수수량']/vol)
                        DATA['current_foreign_ratio'] =current_foreign_ratio
                        if 2*self.collection5.find_one({'stock_code': DATA['단축코드']})['after_foreign_ratio']<current_foreign_ratio:
                            self.bot.sendMessage(chat_id='813531834', text="종목코드  "+  DATA['단축코드']+ "  외국인 순매수 수량 동시간 대비 2시간 이상 증가")
                            if self.collection4.find_one({'stock_code': DATA['단축코드'], '시간': times}):
                                data_input = self.collection4.find_one({'stock_code': DATA['단축코드']}).copy()
                                DATA['_id'] = data_input['_id']
                                self.realTimeLogger.info(self.collection4.replace_one(data_input, DATA, upsert=True))
                            else:
                                self.realTimeLogger.info(self.collection4.insert_one(DATA))

                    if self.collection2.find_one({'단축코드': DATA['단축코드'], '시간': times}):
                        data_input = self.collection2.find_one({'단축코드': DATA['단축코드'], '시간': times}).copy()
                        DATA['_id'] = data_input['_id']
                        self.realTimeLogger.info(self.collection2.replace_one(data_input, DATA, upsert=True))
                        break
                    else:
                        self.realTimeLogger.info(self.collection2.insert_one(DATA))
                        break
            self.realTimeLogger.info("5분 간격 외국인 수급 데이터 저장  후")
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    realTimeForeignVar = SK()
    app.exec_()
