from data.SK import SK

import sys
import time
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from time import sleep

from pymongo import MongoClient
import datetime
from datetime import timedelta
from data.common import mongo_find


if __name__ == "__main__":
    client = MongoClient('127.0.0.1', 27017)
    db = client["stock_data"]
    collection = db["stock_mst"]
    app = QApplication(sys.argv)

    for i in collection.find():
        SK_vari = SK(i["단축코드"])
        time.sleep(0.5)
    app.exec_()

