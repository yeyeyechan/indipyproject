'''
TRAM-ID : SABA655Q1
TR 내용 : 총자산 계좌잔고 조회



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

class stockAccount(QMainWindow):
    def __init__(self,date):

        print("총자산 잔고조회 stockAccount init ")
        super().__init__()
        # 인디의 TR을 처리할 변수를 생성합니다.
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)

        #날짜 설정
        self.date = date
        print("총자산 잔고조회 stockAccount init  finished")
        self.DATA = {}

        #self.market = market
        self.btn_Search()

    # 그럼 실제로 과거 주가를 받아오는 부분은 다음과 같습니다.
    def btn_Search(self):

        # 차트조회 : 과거주가는 차트조회를 통해 받아올 수 있습니다.
        # TR_SCHART : 과거주가를 요청할 TR입니다.
        # 해당 TR의 필드입력형식에 맞춰서 TR을 날리면 됩니다.
        # 데이터 요청 형식
        print("총자산 잔고조회 SABA655Q1 input setup")
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "SABA655Q1")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, "27024779616") # 계좌번호
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1, "01") # 01 종합계좌
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2,   "6930") # 비번
        print("총자산 잔고조회 SABA655Q1 input request")
        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청
    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        print("received SABA655Q1 Data")
        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        print(nCnt+" data received")

        # 받을 열만큼 가거 데이터를 받도록 합니다.
        for i in range(0, nCnt):
            # 데이터 양식
            # 데이터 받기
            self.DATA['순자산평가금액'] = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 0) )# 순자산 평가금액
            self.DATA['총자산평가금액'] = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 1))  # 총자산 평가금액
            self.DATA['주식평가금액'] = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 3))  # 주식 평가금액
            self.DATA['주식제외예수금'] = self.DATA['총자산평가금액'] - self.DATA['주식평가금액']
            print(self.DATA)

        QCoreApplication.instance().exit(0)

    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    activate_Tr = stockAccount( "20200220")
    app.exec_()
