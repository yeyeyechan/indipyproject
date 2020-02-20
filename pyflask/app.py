from flask import Flask, render_template, request, redirect, url_for
from process.buySellProcess import buySellProcess
import sys
from pymongo import MongoClient
from process.autoLogin import autoLogin
from process.autoLogin import autoLoginCheck
from process.realTimeForeign import  realTimeForeign
from PyQt5.QtWidgets import QApplication
from process.show_order_history import show_order_history
from process.buySellModify import buySellModify
import os
import datetime
import time
from analysis.common_data import common_min_shortTime
from analysis.monitoring import  monitoring
from analysis.monitoring2 import  monitoring2
from analysis.monitoring3 import  monitoring3
from analysis.common_data import common_min_timeline
from process.realTimeProgram import realTimeProgram
from process.realTimePrice import realTimePrice
from data.TR_1206 import TR_1206
from data.TR_1314_3 import TR_1314_3
from process.realTimeConclusion import realTimeConclusion
import logging
import logging.handlers
from PyQt5.QtCore import *
'''logging_name = str(datetime.datetime.today().strftime("%Y%m%d"))+"_app.log"
logging.basicConfig(filename='./log/'+logging_name, filemode='a', level= logging.DEBUG, format='[%(levelname)s|%(filename)s:%(lineno)s]%(asctime)s>%(message)s')'''

'''logging_name = str(datetime.datetime.today().strftime("%Y%m%d"))+"_app.log"

logger = logging.getLogger("crumbs")
logger.setLevel(logging.DEBUG)
#logging.basicConfig(filename='./log/'+logging_name, filemode='a', level= logging.DEBUG, format='[%(levelname)s|%(filename)s:%(lineno)s]%(asctime)s>%(message)s')
#vim test kkk

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s',
                                  datefmt='%d/%m/%Y %H:%M:%S')
fileHandler = logging.FileHandler('./log/'+logging_name)
streamHandler = logging.StreamHandler()
fileHandler.setLevel(logging.DEBUG)
streamHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(log_formatter)
streamHandler.setFormatter(log_formatter)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)'''

'''logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")'''
app = Flask(__name__)
print(__name__)
print(sys.argv)
@app.route('/')
def index():
    return render_template('controller.html')


@app.route('/base_monitor/', methods=['POST'])
def base_monitor():
    try:
        date = request.form['date']
        py_time = datetime.datetime.now()
        hour = py_time.hour
        min = py_time.minute
        if (hour == 15 and min >= 30) or hour > 15:
            hour = 15
            min = 30
        # hour = 15
        # min = 35

        total_time = (int)((hour * 60 + min - 9 * 60 - 5) / 5)
        if total_time <= 0:
            total_time = 78
        else:
            total_time += 1
        monitoring3_var = monitoring3(date)
        print("test1")
        monitoring3_var.preprocessProgram()
        time.sleep(2)
        monitoring3_var.preprocessForeign()
        monitoring3_var.preprocessPresent()
        print("test2")
        final_data = monitoring3_var.final_data
        final_data2 = monitoring3_var.final_data2
        final_data3 = monitoring3_var.final_data3
        print("final_data3")
        print(final_data3)
        # total_time = 75
        common_min_timeline_var2 = common_min_shortTime(5).timeline[:total_time]
    except Exception:
        return redirect(url_for('index'))
    return render_template('base_monitor.html', key=final_data.keys(), time_line=common_min_timeline_var2,values=final_data, values2=final_data2, values3=final_data3, length=total_time)

@app.route('/monitoring_test/', methods= ['POST'])
def monitoring_test():
    try:
        py_day = datetime.datetime.today().strftime("%Y%m%d")
        date = request.form['date']

        py_time = datetime.datetime.now()
        hour = py_time.hour
        min = py_time.minute
        if (hour == 15 and min >= 30) or  hour > 15:
            hour = 15
            min = 30
        if py_day != date:
            hour = 15
            min = 30
        #78개임(날) 905-1530
        total_time = (int)((hour*60+min - 9*60 -5)/5)
        if total_time <=0:
            total_time =1
        elif total_time == 77:
            total_time += 1
        else:
            total_time +=2
        #total_time =3
        monitoring3_var = monitoring3(date)
        print("test1")
        monitoring3_var.preprocessProgram()
        time.sleep(2)
        monitoring3_var.preprocessForeign()
        monitoring3_var.preprocessPresent()
        print("test2")
        final_data= monitoring3_var.final_data
        final_data2= monitoring3_var.final_data2
        final_data3= monitoring3_var.final_data3
        print("final_data3")
        print(final_data3)
        #total_time = 75
        common_min_timeline_var2 = common_min_shortTime(5).timeline[:total_time]
    except Exception:
        return redirect(url_for('index'))
    return render_template('monitoring_test.html' , key = final_data.keys() , time_line = common_min_timeline_var2 ,  values= final_data, values2= final_data2, values3 = final_data3 , length = total_time)
@app.route('/monitoring_real/', methods= ['POST'])
def monitoring_real():
    try:
        py_day = datetime.datetime.today().strftime("%Y%m%d")
        date = request.form['date']

        py_time = datetime.datetime.now()
        hour = py_time.hour
        min = py_time.minute
        if (hour == 15 and min >= 30) or  hour > 15:
            hour = 15
            min = 30
        if py_day != date:
            hour = 15
            min = 30
        #78개임(날) 905-1530
        total_time = (int)((hour*60+min - 9*60 -5)/5)
        if total_time <=0:
            total_time =1
        elif total_time == 77:
            total_time += 1
        else:
            total_time +=2
        #total_time =2
        monitoring3_var = monitoring3(date)
        print("test1")
        monitoring3_var.preprocessProgram()
        time.sleep(2)
        monitoring3_var.preprocessForeign()
        monitoring3_var.preprocessPresent()
        print("test2")
        final_data= monitoring3_var.final_data
        final_data2= monitoring3_var.final_data2
        final_data3= monitoring3_var.final_data3
        #total_time = 75
        common_min_timeline_var2 = common_min_shortTime(5).timeline[:total_time]
        final_stock_list = []
        highlight = {

        }
        print(total_time)
        print("total")
        for i in final_data.keys():
            print("ssibal1")
            program_vol = (int)(final_data[i]['프로그램'][total_time-1])
            print("ssibal2")
            print(final_data[i]['프로그램'])
            foreign_vol = (int)(final_data2[i]['외국계순매수수량'][total_time-1])
            print("ssibal20")
            print(final_data2[i]['외국계순매수수량'])
            print("ssibal3")
            print(final_data3[i]['종가'])
            current_value = (int)(final_data3[i]['종가'][total_time-1])
            print("ssibal3")
            print(final_data3[i]['종가'])

            if ((int)(program_vol)>0 and  (int)(foreign_vol)>0 ) and ((int)(program_vol)*(int)(current_value)>20000000 or (int)(foreign_vol)*(int)(current_value)> 20000000):
            #if ((int)(program_vol) > 0 and (int)(foreign_vol) > 0) and ((int)(program_vol) * (int)(current_value) > 2000000 or (int)(foreign_vol) * (int)(current_value) > 2000000):
                final_stock_list.append(i)
                print("sssibballll4")
                if total_time >1 :
                    highlight[i]={

                    }
                    print("check1")
                    highlight[i]['하이라이트']=[]
                    print("check2")
                    for j in range(1, total_time):
                        if (int)(final_data[i]['프로그램'][j-1]) !=0 and (int)(final_data2[i]['외국계순매수수량'][j-1]) !=0:
                            if (int)(final_data[i]['프로그램'][j])/ (int)(final_data[i]['프로그램'][j-1]) >=2.0 and  (int)(final_data2[i]['외국계순매수수량'][j])/ (int)(final_data2[i]['외국계순매수수량'][j-1]) >=2.0:
                                highlight[i]['하이라이트'].append(5000)
                            else:
                                highlight[i]['하이라이트'].append(0)
                        else:
                            highlight[i]['하이라이트'].append(0)
                    print("len(highlight[i]['하이라이트'])")
                    print(len(highlight[i]['하이라이트']))
                    print("len(highlight[i]['하이라이트'])")
                else:
                    print("ssssaaaabbbb")

    except Exception:
        return redirect(url_for('index'))
    return render_template('monitoring_real.html' , key = final_stock_list, time_line = common_min_timeline_var2 ,  values= final_data, values2= final_data2, values3 = final_data3 , length = total_time ,highlight=highlight)


@app.route('/realTimeConclusion/')
def realTimeConclusion_function():
    try:
        realTimeConclusionEvent = QApplication(sys.argv)
        realTimeConclusion_var = realTimeConclusion()
        realTimeConclusionEvent.exec()
    except Exception:
        return  render_template('process_result.html' , message="realTimeConclusion_function 실패")
    return render_template('process_result.html', message="realTimeConclusion_function 실패")

@app.route('/realTime_Price/',  methods = ['POST'])
def realTime_Price():
    date = request.form['date']
    try:
        py_day = datetime.datetime.today().strftime("%Y%m%d")
        date = request.form['date']

        py_time = datetime.datetime.now()
        hour = py_time.hour
        min = py_time.minute
        if (hour == 15 and min >= 30) or  hour > 15:
            hour = 15
            min = 30
        if py_day != date:
            hour = 15
            min = 30
        #78개임(날) 905-1530
        total_time = (int)((hour*60+min - 9*60 -5)/5)
        if total_time <=-1:
            return  render_template('process_result.html' , message="지금은 5분간격 현재가 접수시간이 아닙니다.")
        elif total_time >-1 and total_time<=0:
            total_time =1
        elif total_time==77:
            total_time +=1
        else:
            total_time +=2

        client = MongoClient('127.0.0.1', 27017)
        db = client[date]

        collection_name = date+"_pr_input"
        collection1 = db[collection_name]

        total_len = collection1.count()
        checkIndex = 0
        realTimePriceEvent = QApplication(sys.argv)

        short_time = common_min_shortTime(5)
        print("현재 가장 마지막으로 기록될 현재가 시간은   "+ str(hour)+":"+str(min))
        print("종목의 총 갯수 는 "+ str(total_len))
        print("각종목별 총 기록될 현재가 갯수는 (5분기준 현시각 라스트)     "+str(total_time))
        for i in collection1.find():
            print(i['종목코드'])
            realTimePrice_vari = realTimePrice(i['종목코드'], i['korName'].strip(), '1', '5', "00000000", "99999999",str(total_time),date)
            time.sleep(0.3)
            checkIndex +=1
        if checkIndex != total_time-1:
            realTimePriceEvent.exec()
            print("ssibal")
    except Exception:
        return  render_template('process_result.html' , message="지금은 현재가 데이터 저장 실패")
    return render_template('process_result.html', message="지금은 현재가 데이터 저장 성공")


@app.route('/realTimeProgram/')
def realTimeProgram_start():
    try:
        realTimeProgramEvent = QApplication(sys.argv)
        realTimeProgram_vari = realTimeProgram()
        realTimeProgramEvent.exec_()
    except Exception:
        return redirect(url_for('index'))
    return render_template('program_input.html')
@app.route('/realTimeForeign/')
def realTimeForeign_start():
    try:
        realTimeForeignEvent = QApplication(sys.argv)
        realTimeForeign_vari = realTimeForeign()
        realTimeForeignEvent.exec_()
    except Exception:
        return redirect(url_for('index'))
    return render_template('program_input.html')

@app.route('/realTimeProgram_input/' , methods = ['POST'])
def realTimeProgram_input():
    collection_name =  request.form['date']+"_pr_input"
    client = MongoClient('127.0.0.1', 27017)
    db = client[ request.form['date']]
    collection  = db[collection_name]
    data = {
        "종목코드" : request.form['stock_code'],
        "korName": request.form['korName'],
        "gubun": request.form['gubun']

    }
    collection.insert(data)
    return render_template('program_input.html')

@app.route('/realTimeProgram_input2/' , methods = ['POST'])
def realTimeProgram_input2():
    collection_name = request.form['date']+"_pr_input"
    client = MongoClient('127.0.0.1', 27017)
    db = client[request.form['date']]
    collection_input1 ="TR_1206_5"
    collection_input2 ="TR_1206_2"
    collection_input3 ="TR_1206_3"
    collection  = db[collection_name]
    collection1 = db[collection_input1]
    collection2 = db[collection_input2]
    collection3 = db[collection_input3]
    for i in collection1.find():
        data = {
            "종목코드": i['stock_code'],
            "korName"  : i["korName"],
            "gubun" :i["gubun"]
        }
        collection.insert(data)
        time.sleep(0.3)
    for i in collection2.find():
        data = {
            "종목코드": i['stock_code'],
            "korName"  : i["korName"],
            "gubun" :i["gubun"]
        }
        collection.insert(data)
        time.sleep(0.3)
    for i in collection3.find():
        data = {
            "종목코드": i['stock_code'],
            "korName"  : i["korName"],
            "gubun" :i["gubun"]
        }
        collection.insert(data)
        time.sleep(0.3)
    return render_template('program_input.html')

@app.route('/realTimeProgram_input_page/' , methods = ['POST'])
def realTimeProgram_input_page():

    return render_template('program_input.html', date = request.form['date'])
@app.route('/power_off/')
def power_off():
    os.system("shutdown -s -f")
    return True
@app.route('/mst_SK/', methods = ['POST'])
def mst_SK():
    print("ssibal")
    sk_data = None
    print(True)
    sk_data = request.get_json()
    print(sk_data)
    TR_1206_vari = TR_1206(sk_data['단축코드'], "20200113","20200114", "1","1")

    return True

@app.route('/login/')
def login():
    loginEvent = QApplication(sys.argv)
    autoLoginVar = autoLogin()
    print(autoLoginVar.flag)
    if autoLoginVar.flag:
        return render_template('loginSucess.html')
    else:
        return render_template('loginFailure.html')

@app.route('/autoLogin_Check/')
def autoLogin_Check():
    try:
        autoLoginCheckVar = autoLoginCheck()
        print(autoLoginCheckVar.flag)
        check = autoLoginCheckVar.flag
        if check:
            return render_template('loginSucess.html')
        else:
            return render_template('loginFailure.html')
    except Exception:
        return redirect(url_for('index'))

@app.route('/buy_sell/')
def buy_sell():
    return render_template('buy_sell.html')
'''@app.route('/accounts/' , methods = ['POST'])
def buy_process():
    #return render_template('buy_result.html')

    buy_processEvent = QApplication(sys.argv)
    buySellProcessVar = buySellProcess(request.form['flag'], request.form['stockCode'], request.form['stockQty'],
                                       request.form['stockPrice'], request.form['marketCode'],
                                       request.form['priceCode'])
    buy_processEvent.exec_()
    return render_template("accounts.html", testDataHtml ="실패  " )'''
@app.route('/buy_process/' , methods = ['POST'])
def buy_process():
    #return render_template('buy_result.html')
    try:
        buy_processEvent = QApplication(sys.argv)
        buySellProcessVar = buySellProcess(request.form['flag'], request.form['stockCode'], request.form['stockQty'],
                                           request.form['stockPrice'], request.form['marketCode'],
                                           request.form['priceCode'])
        buy_processEvent.exec_()
        print("result check")
        print(buySellProcessVar.DATA)
        DATA = buySellProcessVar.DATA

        check = DATA["OrderNumber"]
        Message1 = DATA["Message1"]
        Message2 =DATA["Message2"]
        Message3 = DATA["Message3"]
        GetErrorCode = DATA["GetErrorCode"]
        GetErrorMessage = DATA["GetErrorMessage"]
        GetCommState = DATA["GetCommState"]
        message = " 총 주문 금액 "+Message1 + " 가계산 수수료 " + Message2+"  가계산 제세금   "+Message3+"   GetErrorMessage    "+GetErrorMessage

        if (check != '0' or check != None)  and GetErrorCode =="Z0001":
            return render_template("buy_result.html", testDataHtml ="성공  "+ message )
        else:
            return render_template("buy_result.html", testDataHtml ="실패  "+ message )
    except Exception:
        return redirect(url_for('index'))
@app.route('/modify/')
def modify():
    try:
        today = datetime.datetime.today()
        today = today.strftime("%Y%m%d")
        return render_template("modify_page.html" , today = today)
    except Exception:
        return redirect(url_for('index'))
@app.route('/order_list/' , methods = ['POST'])
def order_list():
    try:
        show_order_historyEvent = QApplication(sys.argv)
        show_order_historyVar = show_order_history(request.form['day'])
        show_order_historyEvent.exec_()
        print(True)
        return render_template("order_list_page.html", my_list=show_order_historyVar.DATA_List)
    except Exception :
        return redirect(url_for('index'))


@app.route('/modify_order2/' , methods = ['POST'])
def modify_order2():
    buySellModifyEvent = QApplication(sys.argv)
    try:
        if request.form['원주문번호'] == "0":
            ordercode = request.form['주문번호']
            print('주문번호')
            print(ordercode)
        else:
            ordercode = request.form['원주문번호']
            print('원주문번호')
            print(ordercode)

        buySellModifyVar = buySellModify(request.form['flag'], request.form['출력종목코드'], request.form['주문수량'],
                                         str(int(float(request.form['주문단가']))), request.form['정규시간외구분코드'],
                                         request.form['호가유형코드'], ordercode)
        buySellModifyEvent.exec_()
        DATA = buySellModifyVar.DATA
        print(DATA)
        check = DATA["OrderNumber"]
        Message1 = DATA["Message1"]
        Message2 =DATA["Message2"]
        Message3 = DATA["Message3"]
        GetErrorCode = DATA["GetErrorCode"]
        GetErrorMessage = DATA["GetErrorMessage"]
        GetCommState = DATA["GetCommState"]
        message = " Message1 "+Message1 + " Message2 " + Message2+"  Message3   "+Message3+"   GetErrorMessage    "+GetErrorMessage
        if GetErrorCode =="Z0001":
            return render_template("modify_result.html", testDataHtml ="성공  "+ message )
        else:
            return render_template("modify_result.htm3l", testDataHtml ="실패  "+ message )
    except Exception:
        return redirect(url_for('index'))

@app.route('/modify_order/' , methods = ['POST'])
def modify_order():
    buySellModifyEvent = QApplication(sys.argv)
    buySellModifyVar = buySellModify(request.form['flag'], request.form['stockCode'], request.form['stockQty'],
                                       request.form['stockPrice'], request.form['marketCode'],
                                       request.form['priceCode'], request.form['orderCode'])
    buySellModifyEvent.exec_()
    DATA = buySellModifyVar.DATA

    check = DATA["OrderNumber"]
    Message1 = DATA["Message1"]
    Message2 =DATA["Message2"]
    Message3 = DATA["Message3"]
    GetErrorCode = DATA["GetErrorCode"]
    GetErrorMessage = DATA["GetErrorMessage"]
    GetCommState = DATA["GetCommState"]
    message = " Message1 "+Message1 + " Message2 " + Message2+"  Message3   "+Message3+"   GetErrorMessage    "+GetErrorMessage

    if (check != '0' or check != None)  and GetErrorCode =="Z0001":
        return render_template("modify_result.html", testDataHtml ="성공  "+ message )
    else:
        return render_template("modify_result.html", testDataHtml ="실패  "+ message )
@app.route('/status_page/' )
def status_page():
    try:
        return render_template("status_page.html")
    except Exception:
        redirect(url_for('index'))
@app.route('/foreign_company/' )
def foreign_company():
    try:
        db_name =str(datetime.datetime.today().strftime("%Y%m%d"))
        #db_name = "20200213"
        TR_1314_3Event = QApplication(sys.argv)
        TR_1314_3_vari = TR_1314_3(db_name)
        TR_1314_3Event.exec_()
    except Exception:
        print(Exception)
        return redirect(url_for('index'))
    return render_template("success.html")


@app.route('/get_stock_list/' )
def get_stock_list():
    try:
        db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
        #db_name = "20200213"
        client = MongoClient('127.0.0.1', 27017)
        db = client[db_name]
        collection_data =[]
        collection1 = db["TR_1314_3_2"]
        collection2 = db["TR_1314_3_3"]
        collection3 = db["TR_1314_3_5"]
        collection_status = db["TR_1206_status"]
        collection_status_param = {
            "status": "Processing"
        }
        if collection_status.find():
            collection_status.insert(collection_status_param)
        else:
            for i in collection_status.find():
                try:
                    if i["status"] != "":
                        collection_status.update({
                            "status": i["status"]
                        }, {
                            "status": "Processing"
                        })
                        break
                    else:
                        collection_status.insert(collection_status_param)
                except Exception:
                    print(Exception)
                    return redirect(url_for('index'))
        for i in collection1.find():
            collection_data.append(i)
        for i in collection2.find():
            collection_data.append(i)
        for i in collection3.find():
            collection_data.append(i)
        print("len")
        print(len(collection_data))
        TR_1206Event = QApplication(sys.argv)
        checkindex = 0
        for  i in collection_data:
            if checkindex == len(collection_data):
            #if checkindex == 10:
                #QCoreApplication.exit()
                TR_1206Event.exit(0)
                break
            print(True)
            TR_1206Event_vari = TR_1206(i['단축코드'], '20200218', '20200220','1','0', i['종목명'],  i['구분'], i['구분코드'])
            time.sleep(0.3)
            checkindex +=1
        print(True)
        if checkindex != len(collection_data):
            TR_1206Event.exec_()
        print("True123")
        collection_status.update(collection_status_param, {
            "status": "Success"
        })
        return render_template("success.html")
    except Exception:
        collection_status.update(collection_status_param, {
            "status": "Fail"
        })
        return redirect(url_for('index'))
    return render_template("success.html")

@app.route('/TR_1314_3_result/' )
def TR_1314_3_result():
    try:
        db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
        client = MongoClient('127.0.0.1', 27017)
        db = client[db_name]
        collection = db["TR_1314_status"]
        message = ""
        for i in collection.find():
            if i['status'] == "Processing":
                message="진행중"
                break
            elif i['status'] == "Success":
                message="성공"
                break
            elif   i['status'] == "Fail":
                message="실패"
                break

        return render_template("process_result.html", message =  message )
    except Exception:
        return redirect(url_for('index'))
@app.route('/TR_1206_result/' )
def TR_1206_result():
    try:
        db_name = str(datetime.datetime.today().strftime("%Y%m%d"))
        client = MongoClient('127.0.0.1', 27017)
        db = client[db_name]
        collection = db["TR_1206_status"]
        message = ""
        for i in collection.find():
            if i['status'] == "Processing":
                message="진행중"
                break
            elif i['status'] == "Success":
                message="성공"
                break
            elif   i['status'] == "Fail":
                message="실패"
                break
        return render_template("process_result.html", message =  message )
    except Exception:
        return redirect(url_for('index'))

@app.route('/collect1/')
def collect1():
    try:
        collection_name = str(datetime.datetime.today().strftime("%Y%m%d")) + "_pr_input"
        client = MongoClient('127.0.0.1', 27017)
        db = client[str(datetime.datetime.today().strftime("%Y%m%d"))]
        collection = db[collection_name]
        collection1 = db["TR_1206_1"]
        collection2 = db["TR_1206_2"]
        collection3 = db["TR_1206_3"]

        for i in collection1.find():
            data = {
                "종목코드": i['stock_code']
            }
            collection.insert(data)
            time.sleep(0.3)
        for i in collection2.find():
            data = {
                "종목코드": i['stock_code']
            }
            collection.insert(data)
            time.sleep(0.3)
        for i in collection3.find():
            data = {
                "종목코드": i['stock_code']
            }
            collection.insert(data)
            time.sleep(0.3)
        return render_template("success.html")
    except Exception:
        return redirect(url_for('index'))
@app.route('/getPriceBy5Min/')
def getPriceBy5Min():
    while True:
        time.sleep(300)
        try:
            py_time = datetime.datetime.now()
            hour = py_time.hour
            min = py_time.minute

            if (hour == 15 and min > 30) or hour > 15 or hour < 9:
                print("지금은 현재가 수집 시간 아님!!!")
            else:
                total_time = (int)((hour * 60 + min - 9 * 60 - 5) / 5)

                print("지금 까지 모이는 현재가 데이터 갯수는   "+str(total_time))
                client = MongoClient('127.0.0.1', 27017)
                db = client[str(datetime.datetime.today().strftime("%Y%m%d"))]
                collection_name = str(datetime.datetime.today().strftime("%Y%m%d")) + "_pr_input"
                collection1 = db[collection_name]
                collection2 = db["TR_SCHART_" + str(datetime.datetime.today().strftime("%Y%m%d"))]

                total_len = collection1.count()
                print("현재가를 검색하는 종목의 갯수는   "+str(total_len))

                checkIndex = 0
                realTimePriceEvent = QApplication(sys.argv)

                short_time = common_min_shortTime(5)
                short_time_var = short_time.timeline

                print("현재 가장 마지막으로 기록될 현재가 시간은   " + str(hour) + ":" + str(min))
                print("종목의 총 갯수 는 " + str(total_len))
                print("각종목별 총 기록될 현재가 갯수는 (5분기준 현시각 라스트)     " + str(total_time))
                checkNoFunction = False
                for i in collection1.find():
                    print(i['종목코드'])
                    timeindex = 0
                    for j in short_time_var:
                        if timeindex == 78:
                            break
                        if collection2.find_one({'stock_code': i['종목코드'], 'TIME': j}):
                            print("ssibal")
                            pass
                        else:
                            break
                        timeindex += 1
                    print("total_time-timeindex")
                    print(total_time - timeindex)
                    print("total_time-timeindex")
                    if total_time - timeindex > 0:
                        checkNoFunction = False
                        counts = total_time - timeindex
                        realTimePrice_vari = realTimePrice(i['종목코드'], i['korName'].strip(), '1', '5', "00000000", "99999999",
                                                           str(counts),str(datetime.datetime.today().strftime("%Y%m%d")))
                        time.sleep(0.3)
                    else:
                        print("현재가 데이터 꽉참")
                        checkNoFunction = True
                        pass
                    checkIndex += 1
                if not checkNoFunction:
                    realTimePriceEvent.exec()
                if checkIndex == total_len:
                    print("ssibal")
        except Exception:
            print("fail")


if __name__ == '__main__':
    print(os.getcwd())
    host_addr = "1.232.245.14"
    port_num = "2020"
    app.run(host = host_addr , port = port_num, debug=True)


