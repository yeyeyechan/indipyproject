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
    def __init__(self, date, time_right_now):
        self.realTimeLogger = logging_instance("monitoring_new2.py_ 종목 모니터링 class 시작").mylogger

        self.shortTimeline = common_min_shortTime(5).timeline
        self.date = date

        db_name = self.date

        collection_name1 = db_name+"_pr_input2"
        collection_name2 = "SP_5min_"+db_name
        collection_name3 = "SK_5min_"+db_name
        collection_name4 = "SC_5min_"+db_name
        collection_name5 = "TR_1206_new2_"+db_name

        client = MongoClient('127.0.0.1', 27017)
        db = client[db_name]
        self.realTimeLogger.info("collection 연결 시작 ")
        monitoring_input = db[collection_name1] #인풋 컬렉션
        SP_5min = db[collection_name2] #프로그램 매수 매도 컬렉션
        SK_5min = db[collection_name3] #외국인 매수 매도 컬렉션
        SC_5min = db[collection_name4] #현재가  컬렉션
        TR_1206_new2= db[collection_name5] #현재가  컬렉션
        self.realTimeLogger.info("collection 연결 완료")

        self.monitoring_input = {}
        self.SP_5min = {}
        self.SK_5min = {}
        self.SC_5min = {}
        self.TR_1206_new2 = {}
        self.sorted_monitoring_input = {}

        length = 0
        for i in self.shortTimeline:
            if int(i)<= int(time_right_now):
                length +=1
            else:
                break
        print("ssibal")
        print(length)
        self.timeTimeLine = self.shortTimeline[:length]

        index = 0
        for stock_code_data in monitoring_input.find():
            index +=1
            self.realTimeLogger.info(stock_code_data['종목코드'])
            self.realTimeLogger.info(index)
            self.monitoring_input[stock_code_data['종목코드']] = {}
            self.SP_5min[stock_code_data['종목코드']] = {}
            self.SK_5min[stock_code_data['종목코드']] = {}
            self.SC_5min[stock_code_data['종목코드']] = {}
            self.TR_1206_new2[stock_code_data['종목코드']] = {}
            self.monitoring_input[stock_code_data['종목코드']] = stock_code_data
            for SP_data in SP_5min.find({'단축코드':stock_code_data['종목코드'] }):
                self.SP_5min[stock_code_data['종목코드']][SP_data['sortTime']] = SP_data['비차익위탁프로그램순매수']
            for SK_data in SK_5min.find({'단축코드':stock_code_data['종목코드'] }):
                self.realTimeLogger.info(SK_data)
                self.SK_5min[stock_code_data['종목코드']][SK_data['sortTime']] = SK_data['외국계순매수수량']
            for SC_data in SC_5min.find({'stock_code':stock_code_data['종목코드'] }):
                self.SC_5min[stock_code_data['종목코드']][SC_data['sortTime']] = SC_data['Close']
            for timeTimeLine_data in self.timeTimeLine:
                self.realTimeLogger.info(timeTimeLine_data)
                self.TR_1206_new2[stock_code_data['종목코드']][timeTimeLine_data] = TR_1206_new2.find_one({"stock_code":stock_code_data['종목코드']})['전일외국인순매수거래량']
                self.realTimeLogger.info(self.TR_1206_new2[stock_code_data['종목코드']][timeTimeLine_data])
        print(self.monitoring_input)
        key_list= []
        for keys in self.monitoring_input.keys():
            key_list.append(keys)
        for SK_data in SK_5min.find().sort(['sortTimeInt', pymongo.DESCENDING]):
            if SK_data['단축코드'] in key_list:
                del
            self.sorted_monitoring_input[SK_data['단축코드']] = {}
            self.sorted_monitoring_input[SK_data['단축코드']]= self.monitoring_input[SK_data['단축코드']]
            self.sorted_monitoring_input[SK_data['단축코드']]['외국계순매수수량'] = SK_data['외국계순매수수량']
            self.sorted_monitoring_input[SK_data['단축코드']]['기준시간'] = SK_data['sortTimeInt']
        print(self.sorted_monitoring_input)
if __name__ == "__main__":
    monitoring2_var = monitoring_new2("20200311", "1530")





