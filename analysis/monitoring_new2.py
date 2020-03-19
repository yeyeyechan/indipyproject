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
from analysis.common_data import make_five_min
import pymongo
from datetime import timedelta

class monitoring_new2():
    def __init__(self, date, time_right_now):
        self.realTimeLogger = logging_instance("monitoring_new2.py_ 종목 모니터링 class 시작").mylogger

        self.shortTimeline = common_min_shortTime(5).timeline
        self.date = date

        db_name = self.date

        collection_name1 = db_name+"_pr_input"
        collection_name2 = "SP_5min_"+db_name
        collection_name3 = "SK_5min_"+db_name
        collection_name4 = "SC_5min_"+db_name
        collection_name5 = "TR_1206_"+db_name

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
        Time = make_five_min(time_right_now)
        before_Time = (int)((int)(Time)/100)*60 + (int)(Time)%100 -5
        if (int)(before_Time/60) <10:
            before_Time ="0"+  str((int)(before_Time /60)) + str(before_Time %60)
        else:
            before_Time = str((int)(before_Time /60)) + str(before_Time %60)

        for i in self.shortTimeline:
            if int(i) == int(Time):
                break
            else:
                length +=1
                continue

        self.timeTimeLine = self.shortTimeline[:length+1]

        index = 0


        before_sorted_list = []
        SK_foreign_vol = ''
        for stock_code_data in monitoring_input.find():
            index +=1
            self.realTimeLogger.info(stock_code_data['단축코드'])
            self.realTimeLogger.info(index)
            self.monitoring_input[stock_code_data['단축코드']] = {}
            self.SP_5min[stock_code_data['단축코드']] = {}
            self.SK_5min[stock_code_data['단축코드']] = {}
            self.SC_5min[stock_code_data['단축코드']] = {}
            self.TR_1206_new2[stock_code_data['단축코드']] = {}
            self.monitoring_input[stock_code_data['단축코드']] = stock_code_data
            for SP_data in SP_5min.find({'단축코드':stock_code_data['단축코드'] }):
                self.SP_5min[stock_code_data['단축코드']][SP_data['sortTime']] = SP_data['비차익위탁프로그램순매수']
            for SK_data in SK_5min.find({'단축코드':stock_code_data['단축코드'] }):
                self.realTimeLogger.info(SK_data)
                self.SK_5min[stock_code_data['단축코드']][SK_data['sortTime']] = SK_data['외국계순매수수량']
            for SC_data in SC_5min.find({'단축코드':stock_code_data['단축코드'] }):
                self.SC_5min[stock_code_data['단축코드']][SC_data['sortTime']] = SC_data['Close']
            for timeTimeLine_data in self.timeTimeLine:
                self.realTimeLogger.info(timeTimeLine_data)
                self.TR_1206_new2[stock_code_data['단축코드']][timeTimeLine_data] = TR_1206_new2.find_one({"stock_code":stock_code_data['단축코드']})['전일외국인순매수거래량']
                self.realTimeLogger.info(self.TR_1206_new2[stock_code_data['단축코드']][timeTimeLine_data])
            if SK_5min.find_one({'단축코드': stock_code_data['단축코드'], 'sortTime': Time}) != None:
                SK_foreign_vol =  SK_5min.find_one({'단축코드': stock_code_data['단축코드'], 'sortTime': Time})['외국계순매수수량']
            if SK_5min.find_one({'단축코드': stock_code_data['단축코드'], 'sortTime': Time}) == None and SK_5min.find_one({'단축코드': stock_code_data['단축코드'], 'sortTime': before_Time}) != None :
                SK_foreign_vol =  SK_5min.find_one({'단축코드': stock_code_data['단축코드'], 'sortTime': before_Time})['외국계순매수수량']
            if SK_foreign_vol !=None and SK_foreign_vol != '':
                DATA_before_sorted = {}
                DATA_before_sorted['단축코드'] = stock_code_data['단축코드']
                DATA_before_sorted['외국계순매수수량'] = SK_foreign_vol
                DATA_before_sorted['종목명'] = stock_code_data['종목명']
                DATA_before_sorted['전일대비구분명'] = stock_code_data['전일대비구분명']
                before_sorted_list.append(DATA_before_sorted)
        before_sorted_list  = sorted(before_sorted_list, key = lambda k : k['외국계순매수수량'], reverse= True)
        print(before_sorted_list)
        for i in before_sorted_list:
            self.sorted_monitoring_input[i['단축코드']] = {

            }
            self.sorted_monitoring_input[i['단축코드']] = i
        print(before_sorted_list)

if __name__ == "__main__":
    monitoring2_var = monitoring_new2("20200311", "1530")





