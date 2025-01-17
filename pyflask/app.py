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
app = Flask(__name__)
appLogger = logging_instance("app.py_").mylogger

appLogger.info("Server Start!!!!!!!!!!!!!!!!!!!!!!")
appLogger.info("sys.path")
appLogger.info(sys.path)
appLogger.info("os.getcwd()")
appLogger.info(os.getcwd())


@app.route('/')
def index():
    appLogger = logging_instance("index_").mylogger
    try:
        appLogger.info("index function success")
        return render_template('controller.html')
    except Exception:
        appLogger.error("index function exception occur")
        return render_template('controller.html')
@app.route('/monitoring_new_test3/', methods= ['POST'])
def monitoring_new_test3():
    appLogger = logging_instance("monitoring_new_test3_").mylogger

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
        appLogger.info("monitoring_new2 구동 전")
        monitoring_new_var = monitoring_new2(date)
        appLogger.info("monitoring_new2 구동 후")

        final_data= monitoring_new_var.final_data
        final_data2= monitoring_new_var.final_data2
        final_data3= monitoring_new_var.final_data3
        acc_stock_code= monitoring_new_var.acc_stock_code

        common_min_timeline_var2 = common_min_shortTime(5).timeline[:total_time]
    except Exception:
        return redirect(url_for('index'))
    return render_template('monitoring_test3.html'  , time_line = common_min_timeline_var2 ,  values= final_data, values2= final_data2, values3 = final_data3 ,acc_stock_code=acc_stock_code, length = total_time)

@app.route('/monitoring_new_test2/', methods= ['POST'])
def monitoring_new_test2():
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
        if min <10:
            min = "0"+str(min)
        time_right_now = make_five_min(str(hour)+str(min))
        print("time_right_now")
        print(time_right_now)
        monitoring_new_var = monitoring_new2(date, time_right_now)

        monitoring_input= monitoring_new_var.monitoring_input
        sorted_monitoring_input= monitoring_new_var.sorted_monitoring_input
        SP_5min= monitoring_new_var.SP_5min
        SK_5min= monitoring_new_var.SK_5min
        SC_5min= monitoring_new_var.SC_5min
        TR_1206_new2= monitoring_new_var.TR_1206_new2
        timeTimeLine= monitoring_new_var.timeTimeLine

    except Exception:
        return redirect(url_for('index'))
    return render_template('monitoring_test2.html'  , timeTimeLine = timeTimeLine, monitoring_input = sorted_monitoring_input  , SP_5min = SP_5min , SK_5min = SK_5min , SC_5min = SC_5min, TR_1206_new2 = TR_1206_new2)

@app.route('/monitoring_new_real/', methods= ['POST'])
def monitoring_new_real():
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
        monitoring3_var = monitoring_new(date)


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
    return render_template('process_result.html', message="realTimeConclusion_function 성공")
@app.route('/realTimeAccount/')
def realTimeAccount_function():
    try:
        realTimeAccountEvent = QApplication(sys.argv)
        RealTimeAccount_var = RealTimeAccount()
        realTimeAccountEvent.exec()
    except Exception:
        return  render_template('process_result.html' , message="realTimeAccount_function 실패")
    return render_template('process_result.html', message="realTimeAccount_function 성공")
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

@app.route('/SP_call/')
def SP_call_start():
    appLogger = logging_instance("SP_Call_").mylogger
    try:
        subprocess.call(['sudo', 'python', 'C:\dev\indiPyProject\process\SP.py'])
    except Exception:
        appLogger.error("SP_Call Exception occurs")
        return render_template('process_result.html', message="SP 함수 실행 실패")
    return render_template('process_result.html', message="SP 함수 실행 완료")
@app.route('/SK_call/')
def SK_call_start():

    appLogger = logging_instance("SK_call_").mylogger
    try:
        subprocess.call(['sudo','python', 'C:\dev\indiPyProject\process\SK.py'])
    except Exception:

        appLogger.error("SK_Call Exception occurs")
        return render_template('process_result.html', message="SK 함수 실행 실패")
    return render_template('process_result.html', message="SK 함수 실행 완료")

@app.route('/TR_SCHART_call/')
def TR_SCHART_call_start():
    appLogger = logging_instance("TR_SCHART_call_").mylogger
    try:
        subprocess.call(['sudo','python', 'C:\dev\indiPyProject\process\TR_SCHART.py'])
    except Exception:
        appLogger.error("TR_SCHART_Call Exception occurs")
        return render_template('process_result.html', message="TR_SCHART 함수 실행 실패")
    return render_template('process_result.html', message="TR_SCHART 함수 실행 완료")

@app.route('/realTimeProgram_input/' , methods = ['POST'])
def realTimeProgram_input():
    collection_name =  request.form['date']+"_pr_input2"
    client = MongoClient('127.0.0.1', 27017)
    db = client[ request.form['date']]
    collection  = db[collection_name]
    if  request.form['gubun_code'] == "5":
        gubun = "전일 하락"
    if  request.form['gubun_code'] == "3":
        gubun = "전일 보합"
    if  request.form['gubun_code'] == "2":
        gubun = "전일 상승"
    data = {
        "종목코드" : request.form['stock_code'],
        "korName": request.form['korName'],
        "gubun_code": request.form['gubun_code'],
        "gubun": gubun,
        "연속일자": 0

    }
    collection.insert(data)
    return render_template('program_input.html')

@app.route('/realTimeProgram_input2/' , methods = ['POST'])
def realTimeProgram_input2():
    collection_name = request.form['date']+"_pr_input2"
    client = MongoClient('127.0.0.1', 27017)
    db = client[request.form['date']]
    collection_input1 ="TR_1206_new2_"+request.form['date']

    collection  = db[collection_name]
    collection1 = db[collection_input1]
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
    try:
        loginEvent = QApplication(sys.argv)
        autoLoginVar = autoLogin()
        print(autoLoginVar.flag)
        if autoLoginVar.flag:
            return render_template('loginSucess.html')
        else:
            return render_template('loginFailure.html')
    except Exception:
        return redirect(url_for('index'))

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
    appLogger = logging_instance("buy_sell_").mylogger
    try:
        return render_template('buy_sell.html')
    except Exception:
        appLogger.error("buy_sell function Exception occurs")
        return redirect(url_for('index'))
@app.route('/buy_process/' , methods = ['POST'])
def buy_process():
    appLogger = logging_instance("buy_process_").mylogger
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


        appLogger.debug("inside buy process Event Checking ")

        appLogger.debug("GetErrorCode   "+GetErrorCode)
        appLogger.debug("check   "+check)
        appLogger.debug("GetErrorMessage   "+GetErrorMessage)

        appLogger.debug("inside buy process Event Checking ")

        if (check != '0' or check != None)  and GetErrorCode =="Z0001":
            return render_template("buy_result.html", testDataHtml ="성공  "+ message )
        else:
            return render_template("buy_result.html", testDataHtml ="실패  "+ message )
    except Exception:
        appLogger.error("buy_process Exception occur")
        return redirect(url_for('index'))
@app.route('/modify/')
def modify():
    appLogger = logging_instance("modify_").mylogger
    try:
        today = datetime.datetime.today()
        today = today.strftime("%Y%m%d")
        return render_template("modify_page.html" , today = today)
    except Exception:
        appLogger.error("modify procss Exception occur")
        return redirect(url_for('index'))
@app.route('/order_list/' , methods = ['POST'])
def order_list():
    appLogger = logging_instance("order_list_").mylogger
    try:
        appLogger.info("order_list Event 생성")
        show_order_historyEvent = QApplication(sys.argv)
        show_order_historyVar = show_order_history(request.form['day'])
        show_order_historyEvent.exec_()
        appLogger.info("order_list Event exec")
        return render_template("order_list_page.html", my_list=show_order_historyVar.DATA_List)
    except Exception :
        appLogger.error("order_list procss Exception occur")
        return redirect(url_for('index'))


@app.route('/modify_order2/' , methods = ['POST'])
def modify_order2():
    appLogger = logging_instance("modify_order2_").mylogger

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


        appLogger.debug("inside modify_order2 Event Checking ")

        appLogger.debug("GetErrorCode   "+GetErrorCode)
        appLogger.debug("GetErrorMessage   "+GetErrorMessage)

        appLogger.debug("insidemodify_order2 Event Checking ")

        message = " Message1 "+Message1 + " Message2 " + Message2+"  Message3   "+Message3+"   GetErrorMessage    "+GetErrorMessage
        if GetErrorCode =="Z0001":
            return render_template("modify_result.html", testDataHtml ="성공  "+ message )
        else:
            return render_template("modify_result.html", testDataHtml ="실패  "+ message )
    except Exception:
        appLogger.error("modify_order2 procss Exception occur")
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
@app.route('/foreign_company/'   , methods = ['POST'])
def foreign_company():
    try:
        db_name= request.form['flag']
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
        db_name =request.form['date']
        db_name = "20200302"
        client = MongoClient('127.0.0.1', 27017)
        db = client[db_name]
        collection_data =[]
        collection1 = db["TR_1314_3_2"]
        collection2 = db["TR_1314_3_3"]
        collection3 = db["TR_1314_3_5"]

        for i in collection1.find():
            collection_data.append(i)
        for i in collection2.find():
            collection_data.append(i)
        for i in collection3.find():
            collection_data.append(i)
        TR_1206Event = QApplication(sys.argv)
        checkindex = 0
        for  i in collection_data:
            standard_length = 0
            if checkindex == len(collection_data):
                TR_1206Event.exit(0)
                break
            while standard_length <=2 :
                end_date = db_name
                start_date = datetime.datetime.strptime(end_date, '%Y%m%d') - timedelta(days=standard_length)
                TR_1206Event_vari = TR_1206(i['단축코드'], start_date, end_date,'1','0', i['종목명'],  i['구분'], i['구분코드'], db_name,standard_length)
                time.sleep(0.3)
                standard_length+=1
            checkindex +=1
        if checkindex != len(collection_data):
            TR_1206Event.exec_()

        return render_template("success.html")
    except Exception:
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
    host_addr = "127.0.0.1"
    port_num = "2020"
    app.run(host = host_addr , port = port_num, debug=True)
    print(10)


