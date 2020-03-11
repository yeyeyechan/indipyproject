
# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")
import telegram
import os
import time
from pymongo import MongoClient
from log.logger_pyflask import logging_instance
from analysis.common_data import common_min_shortTime
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from analysis.common_data import make_five_min
import pymongo

def monitoring_report_function():
    telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
    bot = telegram.Bot(token=telgm_token)
    processID = os.getpid()
    realTimeLogger = logging_instance("monitoring_report_function.py_ PID: " + (str)(processID)).mylogger
    realTimeLogger.info("monitoring_report_function 함수 실행 PID: " + (str)(processID))

    client = MongoClient('127.0.0.1', 27017)
    db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
    db = client[db_name]

    monitoring_input = db[db_name+"_pr_input2"]
    SC_check = db["SC_check_"+db_name]
    SK_5min = db["SK_5min_"+db_name]
    SC_5min = db["SC_5min_"+db_name]
    SP_5min = db["SP_5min_"+db_name]

    collection_title2 = "SP_5min_" + str(datetime.datetime.today().strftime("%Y%m%d"))

    time_hour = datetime.datetime.now().hour
    time_min = datetime.datetime.now().minute

    time_now = time_hour*100 +time_min
    TIME = make_five_min(str(time_now))

    for SC_check_data in SC_check.find():
        #if SC_check_data['gubun'] =='2':
        check_first_loop =False
        gubun_code = monitoring_input.find_one({"종목코드": SC_check_data['stock_code']})['gubun_code']
        TR_1206_collection_name = "TR_1206_new_"+ gubun_code
        TR_1206_collection = db[TR_1206_collection_name].find_one({"stock_code" : SC_check_data['stock_code']})
        SK_foreign_vol = ""
        SC_vol         = ""
        #없을시 전꺼루 검색하는 로직 필요
        if SK_5min.find_one({"단축코드": SC_check_data['stock_code'], "sortTime": TIME})!=None and SC_5min.find_one({'stock_code': SC_check_data['stock_code'] , 'sortTime':  TIME})!=None and SC_5min.find_one({'stock_code': SC_check_data['stock_code'] , 'sortTime':  TIME})['Vol']>0 :
            if TR_1206_collection['after_foreign_ratio'] < SK_5min.find_one({"단축코드": SC_check_data['stock_code'], "sortTime": TIME})['외국계순매수수량'] / SC_5min.find_one({'stock_code': SC_check_data['stock_code'] , 'sortTime':  TIME})['Vol']:
                bot.sendMessage(chat_id='813531834', text="종목코드  " +SC_check_data['stock_code'] + "  외국인 순매수 수량 전일 동시간 대비 증가")
                if SP_5min.find_one({"단축코드":SC_check_data['stock_code']}) != None:
                    for SP_data in SP_5min.find({"단축코드":SC_check_data['stock_code']}).sort("sortTimeInt", pymongo.DESCENDING):
                        if SP_data['추세'] == '3':
                            bot.sendMessage(chat_id='813531834', text="종목코드  " + SC_check_data['stock_code'] + "  외국인  순매수 수량 전일 동시간 대비 증가 / 프로그램 순매수 증가 추세")
                        break

        else:
            if SK_5min.find_one({"단축코드": SC_check_data['stock_code'], "sortTime": TIME}) == None:
                for SK_5min_data in SK_5min.find({"단축코드": SC_check_data['stock_code']}).sort("sortTimeInt", pymongo.DESCENDING):
                    SK_foreign_vol = SK_5min_data['외국계순매수수량']
                    break
            if  SC_5min.find_one({'stock_code': SC_check_data['stock_code'], 'sortTime': TIME}) ==None:
                for SC_5min_data in SC_5min.find({"stock_code": SC_check_data['stock_code']}).sort("sortTimeInt",pymongo.DESCENDING):
                    SC_vol = SC_5min_data['Vol']
                    break
            if SC_vol == 0 or SC_vol =="" or SK_foreign_vol =="":
                break
            if TR_1206_collection['after_foreign_ratio'] <SK_foreign_vol/SC_vol :
                bot.sendMessage(chat_id='813531834', text="종목코드  " +SC_check_data['stock_code'] + "  외국인 순매수 수량 전일 동시간 대비 증가")
                if SP_5min.find_one({"단축코드":SC_check_data['stock_code']}) != None:
                    for SP_data in SP_5min.find({"단축코드":SC_check_data['stock_code']}).sort("sortTimeInt", pymongo.DESCENDING):
                        if SP_data['추세'] == '3':
                            bot.sendMessage(chat_id='813531834', text="종목코드  " + SC_check_data['stock_code'] + "  외국인  순매수 수량 전일 동시간 대비 증가 / 프로그램 순매수 증가 추세")
                        break


if __name__ == "__main__":
    monitoring_report_function()
    sched_sc = BlockingScheduler()
    sched_sc.add_job(monitoring_report_function, 'cron', hour ='9-15',minute= '*/1',second='1')
    sched_sc.start()

