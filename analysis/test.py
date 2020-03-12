from pymongo import MongoClient
import datetime
import time
from process.realTimePrice import realTimePrice
from PyQt5.QtWidgets import QApplication
import sys
from analysis.common_data import common_min_shortTime
import telegram
#chat id 813531834

if __name__ == "__main__":
    db_name = "20200312"
    client = MongoClient('127.0.0.1', 27017)
    db = client[db_name]
    collection_name1 = "TR_1206_new_3"
    collection_name2 = "TR_1206_new2_3"
    collection1 = db[collection_name1]
    collection2 = db[collection_name2]

    '''for i in collection1.find():
        if collection2.find_one({"stock_code": i['stock_code']})==None:
            print(" collection2 없으면서 collection1 에 있는거   " + i['stock_code']+ "   종목명   : "+i['korName'] )
            print(collection1.find_one({"stock_code": i['stock_code']}))'''


    for i in collection2.find():
        if collection1.find_one({"stock_code": i['stock_code']})==None:
            print(" collection1에 없으면서 collection2 에 있는거   " + i['stock_code']+ "   종목명   : "+i['korName'])


