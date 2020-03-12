
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import QCoreApplication

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
from log.logger_pyflask import logging_instance
import time
import os
import datetime
class stock_mst(QMainWindow):
    def __init__(self):
        super().__init__()
        self.processID = os.getpid()
        self.realTimeLogger = logging_instance("stock_mst.py_ PID: "+(str)(self.processID)).mylogger
        # 인디의 TR을 처리할 변수를 생성합니다.
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.db_day = str(datetime.datetime.today().strftime("%Y%m%d"))
        client = MongoClient('127.0.0.1', 27017)
        db = client["stock_mst"]
        self.stock_mst = db["stock_mst_collection"]
        self.realTimeLogger.info(" stock_mst tr 호출")
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "stock_mst")
        rqid = self.IndiTR.dynamicCall("RequestData()")

    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        try:
            nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
            self.realTimeLogger.info(" stock_mst tr로 호출된 종목코드 정보 수  "+str(nCnt))
            column = [
                '표준코드               ',
                '단축코드               ',
                '장구분                ',
                '종목명                ',
                'KOSPI200 세부업종      ',
                '결산월일               ',
                '거래정지구분             ',
                '관리구분               ',
                '시장경보구분코드           ',
                '락구분                ',
                '불성실공시지정여부          ',
                '증거금 구분             ',
                '신용증거금 구분           ',
                'ETF 구분자            ',
                '소속구분               '

            ]
            # 받을 열만큼 가거 데이터를 받도록 합니다.
            for i in range(0, nCnt):
                # 데이터 양식
                DATA = {}

                DATA[column[0].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 0)
                DATA[column[1].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 1)
                DATA[column[2].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 2)
                DATA[column[3].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 3)
                DATA[column[4].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 4)
                DATA[column[5].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 5)
                DATA[column[6].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 6)
                DATA[column[7].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 7)
                DATA[column[8].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 8)
                DATA[column[9].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 9)
                DATA[column[10].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 10)
                DATA[column[11].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 11)
                DATA[column[12].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 12)
                DATA[column[13].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 13)
                self.realTimeLogger.info(" stock_mst tr로 호출된 종목코드   " +  DATA[column[1].strip()])

                local_data = self.stock_mst.find_one({"단축코드": DATA[column[1].strip()]})
                if local_data == None:
                    self.stock_mst.insert_one(DATA)
                    self.realTimeLogger.info(self.db_day + " 일자로  "+" stock_mst tr로 새롭게 호출된 종목코드   " + DATA[column[1].strip()])

                else:
                    DATA['_id'] = local_data['_id']
                    self.stock_mst.replace_one(local_data, DATA, upsert=True)
                    self.realTimeLogger.info(self.db_day + " 일자로  "+" stock_mst tr로 호출된 종목코드   " + DATA[column[1].strip()] +" 컬렉션 업데이트 ")
        except Exception:
            self.realTimeLogger.error("stock_mst tr 데이터 정상적으로 처리되지 않음")
        QCoreApplication.exit(0)

    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stock_mst_val = stock_mst()
    app.exec_()
