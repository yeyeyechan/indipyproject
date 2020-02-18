# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from pandas import Series, DataFrame
import pandas as pd
from time import sleep
import threading
import numpy as np
from pymongo import MongoClient
import datetime
from data.common import  weekday_check
from datetime import timedelta
from data.common import mongo_find








if __name__ == "__main__":
    app = QApplication(sys.argv)
    TR_1206_data= mongo_find("stock_data","TR_1206" )
    delta2 = timedelta(days =60)
    for TR_1206_single in TR_1206_data:
        print(TR_1206_single)
        date= TR_1206_single["일자"]
        start_price= TR_1206_single["시가"]
        high_price= TR_1206_single["고가"]
        low_price= TR_1206_single["저가"]
        price= TR_1206_single["가격"]
        standard = TR_1206_single["전일대비구분"]
        diff= TR_1206_single["전일대비"]

        total_vol= TR_1206_single["누적거래량"]
        date= TR_1206_single["개인순매수"]
        date= TR_1206_single["일자"]
        date= TR_1206_single["일자"]
        market = TR_1860_single["market"]
        end_day = TR_1860_single["date"]
        start_day = datetime.datetime.strptime(TR_1860_single["date"], "%Y%m%d").date()
        start_day -= delta2
        start_day = start_day.strftime("%Y%m%d")
        korName = TR_1860_single["korName"]
        print(start_day)
        print(end_day)
        print(1)
        print(stock_code)
        activate_Tr= TR_SCHART(stock_code, korName,  'D', '1', start_day,end_day, '9999',market)
        sleep(1.5)
    app.exec_()
