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
    telgm_token = '1013576743:AAFkCdmafOY61N-I1FAEIEsOdFZwR47_ZQ8'
    bot = telegram.Bot(token=telgm_token)
    updates = bot.getUpdates()
    print(updates)
    for i in updates:
        print(i)

    print('start telegram chat bot')
    bot.sendMessage(chat_id='813531834', text="안녕하세요 시발 채봇입니다.")

    '''date= "20200214"
    py_time =datetime.datetime.now()
    hour = py_time.hour
    min = py_time.minute

    if (hour == 15 and min >= 30) or  hour > 15:
        hour = 15
        min = 35
    total_time = (int)((hour * 60 + min - 9 * 60-5) / 5)

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

    print("현재 가장 마지막으로 기록될 현재가 시간은   "+ str(hour)+":"+str(min))
    print("종목의 총 갯수 는 "+ str(total_len))
    print("각종목별 총 기록될 현재가 갯수는 (5분기준 현시각 라스트)     "+str(total_time))
    for i in collection1.find():
        print(i['종목코드'])
        timeindex = 0
        for j in short_time_var:
            if timeindex ==78:
                break
            print("short_time_var")
            print(j)
            print("short_time_var")
            print("TR_SCHART_"+date)
            print(collection2.find_one({'stock_code': i['종목코드'], 'TIME': j}))
            print("TR_SCHART_"+date)
            if collection2.find_one({'stock_code': i['종목코드'], 'TIME': j}) :
                print("중복")
                pass
            else:
                print("중복 아님")
                break
            timeindex +=1
        print("total_time")
        print(total_time)
        print("total_time")
        print("timeindex")
        print(timeindex)
        print("timeindex")
        print("total_time-timeindex")
        print(total_time-timeindex)
        print("total_time-timeindex")
        if total_time-timeindex >0:
            counts = total_time-timeindex
            realTimePrice_vari = realTimePrice(i['종목코드'], i['korName'].strip(), '1', '5', "00000000", "99999999",str(counts))
            time.sleep(0.3)
        else:
            print("현재가 데이터 꽉참")
            pass
        checkIndex +=1
    realTimePriceEvent.exec()
    if checkIndex == total_len:
        print("ssibal")
        #realTimePriceEvent.exit(0)'''

    '''py_time = datetime.datetime.now()
    hour = py_time.hour
    min = py_time.minute

    if (hour == 15 and min >= 35) or  hour > 15:
        hour = 15
        min = 35

    total_time = (int)((hour * 60 + min - 9 * 60) / 5)
    # hour = 15
    # min = 35
    total_time = (int)((hour * 60 + min - 9 * 60) / 5)
    if total_time <=0:
        total_time = 1
    else:
        total_time += 1

    client = MongoClient('127.0.0.1', 27017)
    db = client[str(datetime.datetime.today().strftime("%Y%m%d"))]
    collection_name = str(datetime.datetime.today().strftime("%Y%m%d"))+"_pr_input"
    collection1 = db[collection_name]
    collection2  = db["TR_SCHART_"+str(datetime.datetime.today().strftime("%Y%m%d"))]
    total_len = collection1.count()
    checkIndex = 0
    realTimePriceEvent = QApplication(sys.argv)

    short_time = common_min_shortTime(5)
    short_time_var = short_time.timeline

    print("현재 가장 마지막으로 기록될 현재가 시간은   "+ str(hour)+":"+str(min))
    print("종목의 총 갯수 는 "+ str(total_len))
    print("각종목별 총 기록될 현재가 갯수는 (5분기준 현시각 라스트)     "+str(total_time))
    for i in collection1.find():
        timeindex = 0
        for j in short_time_var:
            if collection2.find({'stock_code': i['종목코드'], 'TIME': j}):
                print("exist")
                print(collection2.find({'stock_code': i['종목코드'], 'TIME': j}))
                print("exist")
                pass
            else:
                break
            timeindex +=1
        print("total_time-timeindex")
        print(total_time-timeindex)
        print("total_time-timeindex")
        if total_time-timeindex >0:
            counts = total_time-timeindex
            realTimePrice_vari = realTimePrice(i['종목코드'], i['korName'].strip(), '1', '5', "00000000", "99999999",counts)
            time.sleep(0.3)
        else:
            print("현재가 데이터 꽉참")
            pass
    realTimePriceEvent.exit(0)
    if checkIndex != total_len:
        realTimePriceEvent.exec_()'''

