# -*- coding: utf-8 -*-
import sys
from datetime import timedelta

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
import datetime
from data.TR_SCHART import *
from data.TR_1860 import  *
if __name__ == "__main__":
    start = datetime.datetime(2019,1,1)
    end = datetime.datetime(2019,11,19)
    delta = timedelta(days =1)
    delta2 = timedelta(days =60)
    app = QApplication(sys.argv)

    d =  start
    diff=0
    weekend = set([5,6])
    while d <= end:
        if d.weekday() not in weekend:
            cur_day = d.strftime("%Y%m%d")
            before_day = d - delta2
            before_day=before_day.strftime("%Y%m%d")
            print(cur_day)
            stock_code_tr = TR_1860('0', '1', cur_day, "1", "1", '1')
            sleep(1)
            for st_code in stock_code_tr.stock_data['stock_code']:
                TR_SCHART(st_code, 'D', '1', before_day, cur_day, '9999')
                sleep(1)

            print(1)
            print(12)
            diff += 1
        d += delta
    app.exec_()
