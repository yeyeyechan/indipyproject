# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")
from pymongo import MongoClient
import datetime

from analysis.common_data import common_min_timeline
from analysis.common_data import common_min_shortTime
from log.logger_pyflask import logging_instance
import pymongo


class monitoring_new2():
    def __init__(self, date):
        self.realTimeLogger = logging_instance("monitoring_new2.py_ 종목 모니터링 class 시작").mylogger

        self.shortTimeline = common_min_shortTime(5).timeline
        self.date = date

        db_name = self.date

        collection_name1 = db_name+"_pr_input"
        collection_name2 = "SP_5min_"+db_name
        collection_name3 = "SK_5min_"+db_name
        collection_name4 = "SC_5min_"+db_name

        client = MongoClient('127.0.0.1', 27017)
        db = client[db_name]
        self.realTimeLogger.info("collection 연결 시작 ")
        monitoring_input = db[collection_name1] #인풋 컬렉션
        SP_5min = db[collection_name2] #프로그램 매수 매도 컬렉션
        SK_5min = db[collection_name3] #외국인 매수 매도 컬렉션
        SC_5min = db[collection_name4] #현재가  컬렉션
        self.realTimeLogger.info("collection 연결 완료")




if __name__ == "__main__":
    monitoring2_var = monitoring_new2("20200303")





