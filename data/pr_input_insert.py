import sys
import logging
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")
from log.logger_pyflask import logging_instance
from flask import Flask, render_template, request, redirect, url_for
from process.buySellProcess import buySellProcess
from pymongo import MongoClient
from process.autoLogin import autoLogin
from process.autoLogin import autoLoginCheck
from PyQt5.QtWidgets import QApplication
from process.show_order_history import show_order_history
from process.buySellModify import buySellModify
from process.RealTimeAccount import RealTimeAccount
import os
import datetime
import time
from analysis.common_data import common_min_shortTime
from process.realTimePrice import realTimePrice
from data.TR_1206 import TR_1206
from data.TR_1314_3 import TR_1314_3
from process.realTimeConclusion import realTimeConclusion
import subprocess
from analysis.monitoring_new import monitoring_new
from analysis.monitoring_new2 import monitoring_new2
from datetime import timedelta
from analysis.common_data import make_five_min


def TR_1314_3_function() :
    db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
    collection_name = db_name+"_pr_input"
    client = MongoClient('127.0.0.1', 27017)
    db = client[db_name]
    collection_input1 ="TR_1206_new_5"
    collection_input2 ="TR_1206_new_2"
    collection_input3 ="TR_1206_new_3"
    collection  = db[collection_name]
    collection1 = db[collection_input1]
    collection2 = db[collection_input2]
    collection3 = db[collection_input3]
    for i in collection1.find():
        data = {
            "종목코드": i['stock_code'],
            "korName"  : i["korName"],
            "gubun" :i["gubun"],
            "gubun_code" :i["gubun_code"],
            "연속일자": i["연속일자"]

        }
        if collection.find_one({'종목코드': data['종목코드']}):
            data_input =  collection.find_one({'종목코드': data['종목코드']}).copy()
            data['_id'] = data_input['_id']
            collection.replace_one(data_input, data, upsert=True)
        else:
            collection.insert_one(data)
        time.sleep(0.3)
    for i in collection2.find():
        data = {
            "종목코드": i['stock_code'],
            "korName": i["korName"],
            "gubun": i["gubun"],
            "gubun_code": i["gubun_code"],
            "연속일자": i["연속일자"]

        }
        if collection.find_one({'종목코드': data['종목코드']}):
            data_input = collection.find_one({'종목코드': data['종목코드']}).copy()
            data['_id'] = data_input['_id']
            collection.replace_one(data_input, data, upsert=True)
        else:
            collection.insert_one(data)
        time.sleep(0.3)
    for i in collection3.find():
        data = {
            "종목코드": i['stock_code'],
            "korName"  : i["korName"],
            "gubun" :i["gubun"],
            "gubun_code": i["gubun_code"],
            "연속일자": i["연속일자"]

        }
        if collection.find_one({'종목코드': data['종목코드']}):
            data_input =  collection.find_one({'종목코드': data['종목코드']}).copy()
            data['_id'] = data_input['_id']
            collection.replace_one(data_input, data, upsert=True)
        else:
            collection.insert_one(data)
        time.sleep(0.3)
def TR_1406_function() :
    db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
    collection_name = db_name+"_pr_input2"
    client = MongoClient('127.0.0.1', 27017)
    db = client[db_name]
    collection_input1 ="TR_1206_new2_5"
    collection_input2 ="TR_1206_new2_2"
    collection_input3 ="TR_1206_new2_3"
    collection  = db[collection_name]
    collection1 = db[collection_input1]
    collection2 = db[collection_input2]
    collection3 = db[collection_input3]
    for i in collection1.find():
        data = {
            "종목코드": i['stock_code'],
            "korName"  : i["korName"],
            "gubun" :i["gubun"],
            "gubun_code" :i["gubun_code"],
            "연속일자": i["연속일자"]

        }
        if collection.find_one({'종목코드': data['종목코드']}):
            data_input =  collection.find_one({'종목코드': data['종목코드']}).copy()
            data['_id'] = data_input['_id']
            collection.replace_one(data_input, data, upsert=True)
        else:
            collection.insert_one(data)
        time.sleep(0.3)
    for i in collection2.find():
        data = {
            "종목코드": i['stock_code'],
            "korName": i["korName"],
            "gubun": i["gubun"],
            "gubun_code": i["gubun_code"],
            "연속일자": i["연속일자"]

        }
        if collection.find_one({'종목코드': data['종목코드']}):
            data_input = collection.find_one({'종목코드': data['종목코드']}).copy()
            data['_id'] = data_input['_id']
            collection.replace_one(data_input, data, upsert=True)
        else:
            collection.insert_one(data)
        time.sleep(0.3)
    for i in collection3.find():
        data = {
            "종목코드": i['stock_code'],
            "korName"  : i["korName"],
            "gubun" :i["gubun"],
            "gubun_code": i["gubun_code"],
            "연속일자": i["연속일자"]

        }
        if collection.find_one({'종목코드': data['종목코드']}):
            data_input =  collection.find_one({'종목코드': data['종목코드']}).copy()
            data['_id'] = data_input['_id']
            collection.replace_one(data_input, data, upsert=True)
        else:
            collection.insert_one(data)
        time.sleep(0.3)


if __name__ =="__main__":
    TR_1406_function()
