
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
    realTimeLogger = logging_instance("monitoring_report_new3.py_ PID: " + (str)(processID)).mylogger
    realTimeLogger.info("monitoring_report_function 함수 실행 PID: " + (str)(processID))

    client = MongoClient('127.0.0.1', 27017)
    db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
    db = client[db_name]
    TR_1206_collection_name = "TR_1206_new2_" + db_name

    TR_1206_new2 = db["TR_1206_new2_"+db_name]
    SC_check = db["SC_check_"+db_name]
    SK_5min = db["SK_5min_"+db_name]
    SC_5min = db["SC_5min_"+db_name]
    SP_5min = db["SP_5min_"+db_name]
    mesu_check = db["mesu_check_"+db_name]


    time_hour = datetime.datetime.now().hour
    time_min = datetime.datetime.now().minute
    time_now = time_hour*100 +time_min
    TIME = make_five_min(str(time_now))

    for TR_1206_new2_data in TR_1206_new2.find():
        check_foreign_vol =False
        check_program_vol =False
        check_foreign_ratio =False
        check_program_ratio  =False
        #전일 외국인 순매수 거래량
        foreign_vol = TR_1206_new2_data['전일외국인순매수거래량']
        #전일 프로그램 순매수 거래량
        program_vol = TR_1206_new2_data['전일프로그램순매수거래량']
        #전일 개인 순매수 거래량
        personal_vol = TR_1206_new2_data['전일개인순매수거래량']

        # 전일 외국인 순매수 비율
        foreign_ratio = TR_1206_new2_data['전일외국인순매수비율']
        # 전일 프로그램 순매수 비율
        program_ratio = TR_1206_new2_data['전일프로그램순매수비율']
        # 전일 개인 순매수 비율
        personal_ratio = TR_1206_new2_data['전일개인순매수비율']
        #현재가
        if SC_5min.find_one({'stock_code':TR_1206_new2_data['stock_code']}, sort = [('sortTimeInt', pymongo.DESCENDING)]) !=None:
            current_value = SC_5min.find_one({'stock_code': TR_1206_new2_data['stock_code']},sort=[('sortTimeInt', pymongo.DESCENDING)])['Close']
        else:
            current_value = 0

        #현재 외국인 순매수 거래량
        if SK_5min.find_one({'단축코드':TR_1206_new2_data['stock_code']}, sort = [('sortTimeInt', pymongo.DESCENDING)]) !=None:
            current_foreign_vol =  SK_5min.find_one({'단축코드':TR_1206_new2_data['stock_code']}, sort = [('sortTimeInt', pymongo.DESCENDING)])['외국계순매수수량']
        else:
            current_foreign_vol = 0
        #현재 프로그램 순매수 거래량
        if SP_5min.find_one({'단축코드':TR_1206_new2_data['stock_code']}, sort = [('sortTimeInt', pymongo.DESCENDING)]) !=None:
            current_program_vol =  SP_5min.find_one({'단축코드': TR_1206_new2_data['stock_code']}, sort=[('sortTimeInt', pymongo.DESCENDING)])[
                '비차익위탁프로그램순매수']
        else:
            current_program_vol = 0
        #현재 개인 순매수 거래량
        #current_personal_vol =  SC_5min.find_one({'stock_code':TR_1206_new2_data['stock_code']}, sort = [('sortTimeInt', pymongo.DESCENDING)])

        #현재 누적 거래량
        if SP_5min.find_one({'단축코드':TR_1206_new2_data['stock_code']}, sort = [('sortTimeInt', pymongo.DESCENDING)]) !=None:
            current_program_vol =  SP_5min.find_one({'단축코드': TR_1206_new2_data['stock_code']}, sort=[('sortTimeInt', pymongo.DESCENDING)])[
                '비차익위탁프로그램순매수']
        else:
            current_program_vol = 0

        if SC_5min.find_one({'stock_code':TR_1206_new2_data['stock_code']}, sort = [('sortTimeInt', pymongo.DESCENDING)]) !=None:
            current_vol = SC_5min.find_one({'stock_code': TR_1206_new2_data['stock_code']},sort=[('sortTimeInt', pymongo.DESCENDING)])['Vol']
        else:
            current_vol = 0

        # 현재 누적 거래대금
        if  SC_5min.find_one({'stock_code': TR_1206_new2_data['stock_code']}, sort=[('sortTimeInt', pymongo.DESCENDING)]) !=None:
            current_trading_value = SC_5min.find_one({'stock_code': TR_1206_new2_data['stock_code']},
                                                     sort=[('sortTimeInt', pymongo.DESCENDING)])['Trading_Value']
        else:
            current_trading_value = 0

        if current_vol ==0:
            current_foreign_ratio = 0
            current_program_ratio = 0
        else:
            # 현재 외국인 순매수 비율
            current_foreign_ratio = current_foreign_vol /current_vol*100
            #현재 프로그램 순매수 비율
            current_program_ratio = current_program_vol /current_vol*100
        # 전일 외국인 순매수 돌파
        if foreign_vol <current_foreign_vol:
            #bot.sendMessage(chat_id='813531834', text="종목코드  " + TR_1206_new2_data['stock_code'] + " 전일 외국인 순매수 수량 돌파 ")
            check_foreign_vol =True
            # 전일 프로그램 순매수 돌파
            if program_vol <current_program_vol:
                #bot.sendMessage(chat_id='813531834', text="종목코드  " + TR_1206_new2_data['stock_code'] + " 전일 프로그램 순매수 수량 돌파 ")
                check_program_vol = True

        if  current_vol !=0 :
            # 전일 외국인 순매수 비율 돌파
            print("foreign_ratio")
            print(foreign_ratio)
            print("foreign_ratio")
            print("current_foreign_ratio")
            print(current_foreign_ratio)
            print("current_foreign_ratio")
            if foreign_ratio <current_foreign_ratio:
                #bot.sendMessage(chat_id='813531834', text="종목코드  " + TR_1206_new2_data['stock_code'] + " 전일 외국인 순매수 비율 돌파 ")
                check_foreign_ratio = True
                # 전일 프로그램 순매수 비율 돌파
                if program_ratio <current_program_ratio:
                    bot.sendMessage(chat_id='813531834', text="종목코드  " + TR_1206_new2_data['stock_code'] + " 전일  프로그램 /외국인 순매수 비율 돌파 ")
                    check_program_ratio = True
        if (check_foreign_vol and check_program_vol and check_foreign_ratio and check_program_ratio):
            if mesu_check.find_one({"종목코드":TR_1206_new2_data['stock_code'] })== None:
                DATA ={}
                DATA['종목코드'] = TR_1206_new2_data['stock_code']
                DATA['시간']     = TIME
                DATA['최초돌파외국인순매수수량'] = current_foreign_vol
                DATA['최초돌파비차익프로그램순매수수량'] = current_program_vol
                DATA['최초돌파외국인순매수비율'] = current_foreign_ratio
                DATA['최초돌파비차익프로그램순매수비율'] = current_program_ratio
                DATA['최초돌파가격']              =    current_value

                DATA['외국인순매수수량'] = current_foreign_vol
                DATA['비차익프로그램순매수수량'] = current_program_vol
                DATA['외국인순매수비율'] = current_foreign_ratio
                DATA['비차익프로그램순매수비율'] = current_program_ratio
                DATA['가격']              =    current_value
                mesu_check.insert_one(DATA)
                bot.sendMessage(chat_id='813531834', text="종목코드  " + TR_1206_new2_data['stock_code'] + " 매수 추천 지점")
            else:
                if mesu_check.find_one({"종목코드":TR_1206_new2_data['stock_code'] })['최초돌파가격'] > current_value and mesu_check.find_one({"종목코드":TR_1206_new2_data['stock_code'] })['가격'] > current_value and mesu_check.find_one({"종목코드":TR_1206_new2_data['stock_code'] })['외국인순매수수량'] < current_foreign_vol and mesu_check.find_one({"종목코드":TR_1206_new2_data['stock_code'] })['비차익프로그램순매수수량'] < current_program_vol and mesu_check.find_one({"종목코드":TR_1206_new2_data['stock_code'] })['최초돌파외국인순매수수량']  < current_foreign_vol and mesu_check.find_one({"종목코드":TR_1206_new2_data['stock_code'] })['최초돌파비차익프로그램순매수수량'] < current_program_vol :
                    bot.sendMessage(chat_id='813531834',text="종목코드  " + TR_1206_new2_data['stock_code'] + "돌파 시점 보다 가격하락 프로그램 외국인 지속적인 매수 지지 매수 추천  추천가격 : " +str(current_value)+" ~ " + str(mesu_check.find_one({"종목코드":TR_1206_new2_data['stock_code'] })['가격']  ))
                    copied_DATA = mesu_check.find_one({"종목코드":TR_1206_new2_data['stock_code'] }).copy()
                    copied_DATA['외국인순매수수량'] = current_foreign_vol
                    copied_DATA['비차익프로그램순매수수량'] = current_program_vol
                    copied_DATA['외국인순매수비율'] = current_foreign_ratio
                    copied_DATA['비차익프로그램순매수비율'] = current_program_ratio
                    copied_DATA['가격'] = current_value
                    mesu_check.replace_one({'종목코드': TR_1206_new2_data['stock_code']}, copied_DATA)
                    print("Copied_DATA")
                    print(copied_DATA)
                    print("업데이트")

if __name__ == "__main__":
    monitoring_report_function()
    sched_sc = BlockingScheduler()
    sched_sc.add_job(monitoring_report_function, 'cron', hour ='9-15',minute= '*/1',second='1')
    sched_sc.start()

