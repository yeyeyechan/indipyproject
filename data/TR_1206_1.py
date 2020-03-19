'''
PROTOCOL
TRAN-ID	TR_1260	TR구분	XMFTR
	TR 내용	상한가/하한가 종목 조회

INPUT FIELD
Field#	항 목 명	SIZE	항 목 내 용 설 명
【Single 데이터】
0	    단축코드	6
1	    시작일	    8	Ex>20080101
2	    종료일	    8	Ex>20080912
3	    조회구분	1	“1” : 전체, “”:60개
4	    데이터 종류 구분	1	0:거래량 		1:거래대금


'''

# -*- coding: utf-8 -*-
import sys
from asyncio import Event
from threading import Condition
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")
from datetime import timedelta
from pytimekr import pytimekr
from analysis.common_data import get_endDay
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
import datetime
from pymongo import MongoClient
import time
from PyQt5.QtCore import *

class TR_1206_1(QMainWindow):
    def __init__(self, stock_code, start_date, end_date, counts, data_type, korName,date, standard_length):
        super().__init__()
        self.stock_code  = stock_code # 주식코드
        self.korName  = korName # 한글 이름
        self.start_date  = start_date # 시작일
        self.end_date  = end_date # 마지막일

        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)


        self.standard_length = standard_length
        self.flag = False
        client = MongoClient('127.0.0.1', 27017)
        db_name = date
        db = client[db_name]
        collection_name = "TR_1206_"+date
        input1_collection_name = date + "_pr_input"
        self.input = db[input1_collection_name]
        self.TR_1206 = db[collection_name] #TR_1206_1
        self.columnName = {
            '1': "일자                           ",
            '2': "가격                           ",
            '3': "시가                           ",
            '4': "고가                           ",
            '5': "저가                           ",
            '6': "전일대비구분                   ",
            '7': "전일대비                       ",
            '8': "누적거래량                     ",
            '9': "개인매수거래량                 ",
            '10': "개인매도거래량                 ",
            '11': "개인순매수거래량               ",
            '12': "개인매수누적                   ",
            '13': "개인매도누적                   ",
            '14': "개인순매수누적거래량           ",
            '15': "외국인매수거래량               ",
            '16': "외국인매도거래량               ",
            '17': "외국인순매수거래량             ",
            '18': "외국인매수누적                 ",
            '19': "외국인매도누적                 ",
            '20': "외국인순매수누적거래량         ",
            '21': "기관매수거래량                 ",
            '22': "기관매도거래량                 ",
            '23': "기관순매수거래량               ",
            '24': "기관매수누적                   ",
            '25': "기관매도누적                   ",
            '26': "기관순매수누적거래량           ",
            '27': "금융투자매수거래량             ",
            '28': "금융투자매도거래량             ",
            '29': "금융투자순매수거래량           ",
            '30': "금융투자매수누적               ",
            '31': "금융투자매도누적               ",
            '32': "금융투자순매수누적거래량       ",
            '33': "투신매수거래량                 ",
            '34': "투신매도거래량                 ",
            '35': "투신순매수거래량               ",
            '36': "투신매수누적                   ",
            '37': "투신매도누적                   ",
            '38': "투신순매수누적거래량           ",
            '39': "은행매수거래량                 ",
            '40': "은행매도거래량                 ",
            '41': "은행순매수거래량               ",
            '42': "은행매수누적                   ",
            '43': "은행매도누적                   ",
            '44': "은행순매수누적거래량           ",
            '45': "기타금융매수거래량             ",
            '46': "기타금융매도거래량             ",
            '47': "기타금융순매수거래량           ",
            '48': "기타금융매수누적               ",
            '49': "기타금융매도누적               ",
            '50': "기타금융순매수누적거래량       ",
            '51': "보험매수거래량                 ",
            '52': "보험매도거래량                 ",
            '53': "보험순매수거래량               ",
            '54': "보험매수누적                   ",
            '55': "보험매도누적                   ",
            '56': "보험순매수누적거래량           ",
            '57': "기금매수거래량                 ",
            '58': "기금매도거래량                 ",
            '59': "기금순매수거래량               ",
            '60': "기금매수누적                   ",
            '61': "기금매도누적                   ",
            '62': "기금순매수누적거래량           ",
            '63': "기타매수거래량                 ",
            '64': "기타매도거래량                 ",
            '65': "기타순매수거래량               ",
            '66': "기타매수누적                   ",
            '67': "기타매도누적                   ",
            '68': "기타순매수누적거래량           ",
            '69': "외국인기타매수거래량           ",
            '70': "외국인기타매도거래량           ",
            '71': "외국인기타순매수거래량         ",
            '72': "외국인기타매수누적             ",
            '73': "외국인기타매도누적             ",
            '74': "외국인기타순매수누적거래량     ",
            '75': "국가지자체매수거래량           ",
            '76': "국가지자체매도거래량           ",
            '77': "국가지자체순매수거래량         ",
            '78': "국가지자체매수누적             ",
            '79': "국가지자체매도누적             ",
            '80': "국가지자체순매수누적거래량     ",
            '81': "프로그램매수                   ",
            '82': "프로그램매도                   ",
            '83': "프로그램순매수                 ",
            '84': "프로그램누적매수               ",
            '85': "프로그램누적매도               ",
            '86': "프로그램누적순매수             ",
            '87': "사모펀드매수                   ",
            '88': "사모펀드매도                   ",
            '89': "사모펀드순매수                 ",
            '90': "사모펀드누적매수               ",
            '91': "사모펀드누적매도               ",
            '92': "사모펀드누적순매수             ",
            '93': "전일대비율                     ",
            '94': "외국인지분율                   "
        }

        self.stock_code= stock_code
        self.start_date= start_date
        self.end_date= end_date
        self.counts= counts
        self.end_date= end_date
        self.counts= counts
        self.data_type = data_type
        self.btn_Search()
    def btn_Search(self):
        # 조회할 종목의 이름을 받아옵니다.

        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "TR_1206")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.stock_code)  # 인풋 : 단축 코드
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 1,self.start_date)  # 인풋 : 시작일 8 자리
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 2, self.end_date)  # 인풋 : 종료일 8 자리
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 3, self.counts)  # 인풋 : 조회구분 1: 전체  "" : 60개
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 4,  self.data_type)  # 인풋 : 0 :거래량 1: 거래대금
        rqid = self.IndiTR.dynamicCall("RequestData()")
        print(rqid)
        print("btn_search")
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.

        DATA = {}
        old_total_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 2, 7))
        old_val = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 2, 1))
        old_trans_ammount = old_total_vol*old_val

        cum_old_personal_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 2, 13))
        cum_old_foreign_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 2, 19))
        old_gubun = self.IndiTR.dynamicCall("GetMultiData(int, int)", 2, 5)
        old_foreign_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 2, 16))
        old_personal_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 2, 10))
        old_program_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 2, 82))

        before_total_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 1, 7))
        before_val = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 1, 1))
        before_trans_ammount = before_total_vol*before_val
        before_total_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 1, 7))
        before_personal_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 1, 10))
        cum_before_personal_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 1, 13))
        cum_before_foreign_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 1, 19))
        before_foreign_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 1, 16))
        before_program_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 1, 82))
        before_gubun = self.IndiTR.dynamicCall("GetMultiData(int, int)", 1, 5)

        if before_total_vol ==0:
            self.flag = True
            print(self.flag)
            #QCoreApplication.instance().exit(0)
            return "ok"
        before_personal_ratio = (int)(before_personal_vol/before_total_vol *100)
        before_foreign_ratio = (int)(before_foreign_vol/before_total_vol *100)
        before_program_ratio = (int)(before_program_vol/before_total_vol *100)


        after_total_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 0, 7))
        after_val = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 0, 1))
        after_trans_ammount = after_total_vol*after_val
        after_total_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 0, 7))
        after_personal_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 0, 10))
        cum_after_personal_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 0, 13))
        cum_after_foreign_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 0, 19))
        after_foreign_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 0, 16))
        after_program_vol = (int)(self.IndiTR.dynamicCall("GetMultiData(int, int)", 0, 82))
        after_gubun = self.IndiTR.dynamicCall("GetMultiData(int, int)", 0, 5)

        if after_total_vol ==0:
            self.flag = True
            print(self.flag)
            return "ok"
        after_personal_ratio = (int)(after_personal_vol/after_total_vol *100)
        after_foreign_ratio = (int)(after_foreign_vol/after_total_vol *100)
        after_program_ratio = (int)(after_program_vol/after_total_vol *100)

        if old_personal_vol >0 and old_foreign_vol <0 and old_program_vol <0 and old_trans_ammount > 9000000000:
            if before_personal_vol <0 and before_foreign_vol >0 and before_program_vol >0 and before_trans_ammount > 9000000000:
                if after_personal_vol < 0  and -10*before_personal_vol < -1*after_personal_vol and -10*before_personal_ratio < -1*after_personal_ratio and after_trans_ammount > 9000000000:
                    if after_foreign_vol >0 and after_program_vol >0 and 10*before_foreign_vol < after_foreign_vol and 10*before_program_vol < after_program_vol and 10*before_foreign_ratio < after_foreign_ratio and 10*before_program_ratio < after_program_ratio:
                        if -0.9* after_personal_vol < after_foreign_vol and 0.9*after_program_vol < after_foreign_vol:
                            DATA['전일거래량'] = after_total_vol  #
                            DATA['전일개인순매수거래량'] = after_personal_vol  #
                            DATA['전일외국인순매수거래량'] = after_foreign_vol  #
                            DATA['전일프로그램순매수거래량'] = after_program_vol  #
                            DATA['전일개인순매수비율'] = after_personal_ratio  #
                            DATA['전일외국인순매수비율'] = after_foreign_ratio  #
                            DATA['전일프로그램순매수비율'] = after_program_ratio  #
                            DATA['전일추정거래대금'] = after_trans_ammount  #

                            DATA['단축코드'] = self.stock_code  # 주식코드
                            DATA['전일대비구분'] = self.IndiTR.dynamicCall("GetMultiData(int, int)", 0, 5)
                            DATA['로직구분']        =   "1"
                            if DATA['전일대비구분'] == "3":
                                DATA['전일대비'] = "전일 보합"
                            elif DATA['전일대비구분'] == "2":
                                DATA['전일대비'] = "전일 상승"
                            elif DATA['전일대비구분'] == "5":
                                DATA['전일대비'] = "전일 하락"
                            DATA['종목명'] = self.korName
                            DATA['시작일'] = self.start_date  # 시작일
                            DATA['마지막일'] = self.end_date  # 마지막일
                            DATA['연속일자'] = self.standard_length
                            print("TR_1206 데이터 적재")
                            print(self.TR_1206.insert_one(DATA))
                            print("TR_1206 데이터 적재")

                            data = {
                                "단축코드": self.stock_code,
                                "종목명": self.korName,
                                "전일대비":DATA['gubun'] ,
                                "전일대비구분": DATA['gubun_code'],
                                "연속일자":self.standard_length,
                                "로직구분": DATA['로직구분']

                            }
                            if self.input.find_one({'단축코드': data['단축코드']}):
                                data_input = self.input1.find_one({'단축코드': data['단축코드']}).copy()
                                data['_id'] = data_input['_id']
                                print("input1 데이터 업뎃")
                                self.input.replace_one(data_input, data, upsert=True)
                                print("input1 데이터 업뎃")
                            else:
                                print("input1 데이터 적재")
                                self.input.insert_one(data)
                                print("input1 데이터 적재")
                            self.flag = True
                        else:
                            return
                    else:
                        return
                else:
                    return
            else:
                return
        else:
            return
        return

    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)
def check_next(function_vari):
    if function_vari =="ok":
        return True

if __name__ == "__main__":
    db_name = "20200319"
    client = MongoClient('127.0.0.1', 27017)
    db = client["stock_mst"]
    collection_data = []
    collection1 = db["stock_mst_collection"]
    for i in collection1.find():
        collection_data.append(i)
    TR_1206Event = QApplication(sys.argv)
    checkindex = 0
    end_date= get_endDay(db_name)

    for i in collection_data:
        standard_length = 0
        if checkindex == len(collection_data):
            TR_1206Event.exit(0)
        checkindex += 1
        TR_1206_vari = TR_1206_1(i['단축코드'], "20200316", "20200318", '1', '0', i['종목명'], db_name, standard_length)
        time.sleep(0.3)

    if checkindex != len(collection_data):
        TR_1206Event.exec_()


