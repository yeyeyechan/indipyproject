# -*- coding: utf-8 -*-
import sys
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
import time
'''
    신한아이 인디 자동로그인 예제
'''

class autoLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.flag= False
        start = time.time()

        # 일반 TR OCX
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")

        # 신한i Indi 자동로그인
        while True:
            if time.time() - start >=100:
                QCoreApplication.exit(0)
            login = self.IndiTR.StartIndi('xamevh123', 'florida1!23', 'florida1!23', 'C:\SHINHAN-i\indi\giexpertstarter.exe')
            print(login)
            if login == True :
                self.flag = True
                QCoreApplication.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    IndiWindow = autoLogin()
    print("test")
    print(IndiWindow.flag)
    app.exec_()