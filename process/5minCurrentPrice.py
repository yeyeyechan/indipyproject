import sys
from pymongo import MongoClient

from PyQt5.QtWidgets import QApplication

import time as pytime
from analysis.common_data import common_min_shortTime

from process.realTimePrice import realTimePrice
from datetime import time, datetime
import threading

class minCurrentPrice():
    def __init__(self):
        pass
    def fiveMinCurrentPrice(self):

        morning = time(0, 50)
        evening = time(1, 30)
        now = datetime.now().time()  # 일시 객체
        dt = datetime.now()
        #date =str(datetime.today().strftime("%Y%m%d"))
        date = "20200217"
        if morning <= now and evening > now:
            py_time =datetime.now()
            hour = py_time.hour
            min = py_time.minute
            #total_time = (int)((hour * 60 + min - 9 * 60-5) / 5)
            total_time = (int)((hour * 60 + min -50) / 5)
            total_time +=1
            client = MongoClient('127.0.0.1', 27017)
            db = client[date]
            collection_name = date+"_pr_input"
            collection1 = db[collection_name]
            collection2  = db["TR_SCHART_"+date]
            total_len = collection1.count()
            checkIndex = 0
            realTimePriceEvent = QApplication(sys.argv)

            short_time = common_min_shortTime(5)
            short_time_var = short_time.timeline
            checkNoFunction = False
            print("현재 가장 마지막으로 기록될 현재가 시간은   "+ str(hour)+":"+str(min))
            print("종목의 총 갯수 는 "+ str(total_len))
            print("각종목별 총 기록될 현재가 갯수는 (5분기준 현시각 라스트)     "+str(total_time))
            for i in collection1.find():
                print(i['종목코드'])
                timeindex = 0
                for j in short_time_var:
                    if timeindex == 78:
                        break
                    print("j")
                    print(j)
                    print("j")
                    if collection2.find_one({'stock_code': i['종목코드'], 'TIME': j}) :
                        print("중복")
                        pass
                    else:
                        print("중복 아님")
                        break
                    timeindex +=1
                print("total_time-timeindex")
                print(total_time-timeindex)
                print("total_time-timeindex")
                if total_time-timeindex >0:
                    counts = total_time-timeindex
                    checkNoFunction =False
                    realTimePrice_vari = realTimePrice(i['종목코드'], i['korName'].strip(), '1', '5', "00000000", "99999999",str(counts),date)
                    pytime.sleep(0.3)
                else:
                    print("현재가 데이터 꽉참")
                    checkNoFunction =True
                    pass
                checkIndex +=1
            if not checkNoFunction:
                realTimePriceEvent.exec()
            if checkIndex == total_len:
                print("ssibal")


        else:
            print("not now")
        print('sync Function OK (%s)' % dt + '\n')
        threading.Timer(100, self.fiveMinCurrentPrice).start()

def main():
    at = minCurrentPrice()
    at.fiveMinCurrentPrice()

if __name__ == '__main__':
    main()