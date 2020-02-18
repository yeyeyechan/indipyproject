from pymongo import MongoClient
from pytimekr import pytimekr
import datetime
import pymongo
if __name__ == "__main__":
    kr_holidays = pytimekr.holidays()
    datetime.date
    start = datetime.datetime(2019,1,1)

    if start.date() not in kr_holidays:
        print(type(start))