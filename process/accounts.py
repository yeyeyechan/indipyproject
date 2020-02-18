import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
import socket
import requests
import time
class SABA609Q1(QMainWindow):

    def __init__(self ):
        super().__init__()


        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)

        # 데이터 양식
        self.DATA = {}
        self.startProcess()
    # 그럼 실제로 과거 주가를 받아오는 부분은 다음과 같습니다.
    def startProcess(self):
        # 데이터 요청 형식
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "SABA609Q1")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, "27024779616") # 계좌번호
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1, "01") # 계좌상품 항상 01
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, "6930") #계좌 비밀번호
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3, "1")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 4, "1")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 5, "0") #
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 6, "0")

        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청


    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        print(True)

        print( self.IndiTR.dynamicCall("GetErrorState()"))
        print( self.IndiTR.dynamicCall("GetErrorCode()"))
        print( self.IndiTR.dynamicCall("GetErrorMessage()"))
        print( self.IndiTR.dynamicCall("GetCommState()"))
        # 데이터 받기
        self.DATA['OrderNumber'] = self.IndiTR.dynamicCall("GetSingleData(int)", 0)  # 주문번호
        self.DATA['ORCOrderNumber'] = self.IndiTR.dynamicCall("GetSingleData(int)", 1)  # ORC 주문번호
        self.DATA['Message'] = self.IndiTR.dynamicCall("GetSingleData(int)", 2)  # Message 구분
        self.DATA['Message1'] = self.IndiTR.dynamicCall("GetSingleData(int)", 3)  # Message1
        self.DATA['Message2'] = self.IndiTR.dynamicCall("GetSingleData(int)", 4)  # Message2
        self.DATA['Message3'] = self.IndiTR.dynamicCall("GetSingleData(int)", 5)  # Message3


        self.DATA['GetErrorState'] = self.IndiTR.dynamicCall("GetErrorState()")
        self.DATA['GetErrorCode'] = self.IndiTR.dynamicCall("GetErrorCode()")
        self.DATA['GetErrorMessage'] =self.IndiTR.dynamicCall("GetErrorMessage()")
        self.DATA['GetCommState'] = self.IndiTR.dynamicCall("GetCommState()")

        print(self.DATA)
        QCoreApplication.instance().quit()
        # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
    def kill(self):
        del self

if __name__ == "__main__":
    app = QApplication(sys.argv)
    buySellProcessVar = buySellModify("2", "A055550","1","42800","1", "2")
    print("buySellProcessVar.check")
    print(buySellProcessVar.check)
    sys.exit(app.exec_())
