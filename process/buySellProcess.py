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
class buySellProcess(QMainWindow):

    def __init__(self ,  flag, stockCode, stockQty, stockPrice, marketCode, priceCode ):
        super().__init__()


        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)

        self.flag = flag
        self.stockCode = stockCode
        self.stockQty = stockQty
        self.stockPrice = stockPrice
        self.marketCode = marketCode
        self.priceCode = priceCode

        self.check = False
        print("test1")
        print( self.flag)
        print(self.stockCode )
        print(self.stockQty )
        print(self.stockPrice )
        print(self.marketCode )
        print(self.priceCode)


        # 데이터 양식
        self.DATA = {}
        self.startProcess()
    # 그럼 실제로 과거 주가를 받아오는 부분은 다음과 같습니다.
    def startProcess(self):
        # 데이터 요청 형식
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "SABA101U1")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, "27024779616") # 계좌번호
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1, "01") # 계좌상품 항상 01
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, "6930") #계좌 비밀번호
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 5, "0") # 선물대용매도여부 0 일반
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 6, "00") # 신용거래구분 00 보통
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 7, self.flag) # 매수 매도 구분 1 매도 2 매수
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 8, self.stockCode) # 종목코드 현물 단축코드에 A 포함 ELW J ETN Q
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 9, self.stockQty) #주문수량
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 10, self.stockPrice) # 주문가격 장전시간외, 시간외 종가 주문시 "0"
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 11, self.marketCode) # 정규 시간외 구분코드 1 정규장, 2 장개시전시간외 3 장종료후 시간외 종가 4 장종료후 시간외단일가 5 장종료후 시간외 대량
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 12, self.priceCode) # 호가 유형코드 1 시장가 2지정가 1 조건부지정가 X 최유리 Y 최우선 Z 변동없음(정정주문시)
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 13, "0") # 주문 조건 코드 0 일반 3 IOC 4 FOK
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 14, "0") # 신용 대출 통합 주문 구분 코드 0 해당 없음 1 대출일 2 선입선출 3 후입선출
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 21, "Y") # Y 로 설정한 경우에 한하여 output message 1,2,3 출력
        print("Test2")
        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청
        print("Test3")
        print(rqid)

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

        if self.DATA['OrderNumber'] =='0':
            self.check =False
        else:
            self.check = True
        print(self.DATA)
        QCoreApplication.instance().quit()
        # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
    def kill(self):
        del self

if __name__ == "__main__":
    app = QApplication(sys.argv)
    buySellProcessVar = buySellProcess("2", "A055550","1","42800","1", "2")
    print("buySellProcessVar.check")
    print(buySellProcessVar.check)
    sys.exit(app.exec_())
