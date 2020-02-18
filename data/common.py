from datetime import timedelta

from pytimekr import pytimekr
from pymongo import MongoClient
import datetime


'''
한국 주식 거래일 구하는 함수
day 형식 datetime.datetime
'''
def weekday_check(day):
    weekend = set([5,6])
    kr_holidays = pytimekr.holidays()
    if (day.weekday() not in weekend) and (day.date() not in kr_holidays):
        return True
    return False

def mongo_find(db_name, collection_name):
    client = MongoClient('127.0.0.1', 27017)
    db = client[db_name]
    collection = db[collection_name]

    return collection.find()

