import sys
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from datetime import datetime
from log.logger_pyflask import logging_instance
from analysis.common_data import common_min_shortTime

class show_order_history(QMainWindow):
    def __init__(self ,  day):
        super().__init__()
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.realTimeLogger = logging_instance("show_order_history.py 주문 체결/미체결 내역 조회").mylogger
        self.day = day
        self.DATA_List = list()
        self.DATA ={

        }
        self.check = False

        # 데이터 양식
        self.realTimeLogger.info("startProcess 호출")
        self.startProcess()
    # 그럼 실제로 과거 주가를 받아오는 부분은 다음과 같습니다.
    def startProcess(self):
        # 데이터 요청 형식
        self.realTimeLogger = logging_instance("show_order_history.py 주문 체결/미체결 내역 조회").mylogger
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "SABA231Q1")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.day) # 매매일자
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1, "27024779616") # 계좌번호
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, "6930") #계좌 비밀번호
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3, "00") # 장구분 00:전체  		01:KOSPI 02:KOSDAQ 		03:OTCBB  04:ECN  		05:단주  11:매도주문  		12:매수주문
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 4, "00") # 체결구분 0:전체  		1:체결  2:미체결
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 5, "0") # 0:합산(주문건별 합산)  	1:건별(체결건)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 6, "*") # 입력 종목 코드 * 전체
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 7, "01") # 작업자 사번?
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 8, "Y") #

        self.realTimeLogger.info("SABA231Q1 RequestData 호출 전")
        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청
        self.realTimeLogger.info("SABA231Q1 RequestData 호출 후")

    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        self.realTimeLogger = logging_instance("show_order_history.py 주문 체결/미체결 내역 조회").mylogger

        if rqid == "SABA231Q1":
            # 데이터 받기
            nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
            for i in range(0, nCnt):
                self.realTimeLogger.info("SABA231Q1 data received")
                # 데이터 양식
                DATA = {
                }
                DATA['주문번호'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 0)
                DATA['원주문번호'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 1)
                DATA['시장거래구분'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 2)
                DATA['정규시간외구분코드'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 8)
                DATA['호가유형코드'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 9)
                DATA['출력종목코드'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 13)
                DATA['종목명'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 14)
                DATA['주문수량'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 15)
                DATA['주문단가'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 16)
                DATA['미체결수량'] = self.IndiTR.dynamicCall("GetMultiData(int , int)", i, 26)
                self.DATA_List.append(DATA)
        else:
            self.realTimeLogger.info("SABA231Q1 data not received")
            QCoreApplication.instance().quit(0)
        self.realTimeLogger.info("Call Qapplication instance quit ")
        QCoreApplication.instance().quit(0)
        # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        self.realTimeLogger = logging_instance("show_order_history.py 주문 체결/미체결 내역 조회").mylogger
        self.realTimeLogger.info("System Message received")
        self.realTimeLogger.info("System Message Received = MsgID "+ MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    buySellProcessVar = show_order_history("20191230")
    app.exec_()
