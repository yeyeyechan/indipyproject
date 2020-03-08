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

class TR_1206(QMainWindow):
    #def __init__(self, stock_code , start_date, end_date, counts, data_type , korName , market):
    def __init__(self, stock_code, start_date, end_date, counts, data_type, korName, gubun, gubun_code,date, standard_length):

        super().__init__()
        print("init")
        self.stock_code  = stock_code # 주식코드
        self.korName  = korName # 한글 이름
        self.gubun  = gubun # gubun
        self.gubun_code  = gubun_code #  gubun_code
        self.start_date  = start_date # 시작일
        self.end_date  = end_date # 마지막일
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)
        self.standard_length = standard_length

        client = MongoClient('127.0.0.1', 27017)
        db_name = date
        db = client[db_name]
        collection_name = "TR_1206_"+self.gubun_code

        self.collection1 = db[collection_name] #TR_1206_1
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
        print(self.stock_code)
        print(self.start_date)
        print(self.end_date)
        print(self.counts)
        print(self.data_type)

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

        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        nCnt = self.IndiTR.dynamicCall("GetMultiRowCount()")
        list = []
        check =0
        for i in range(0, nCnt):
            # 데이터 양식
            DATA = {}
            '''DATA[self.columnName['1'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int )", i, 0)
            DATA[self.columnName['2'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int )", i, 1)
            DATA[self.columnName['3'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int )", i, 2)
            DATA[self.columnName['4'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int )", i, 3)
            DATA[self.columnName['5'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int )", i, 4)
            DATA[self.columnName['6'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int )", i, 5)
            DATA[self.columnName['7'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int )", i, 6)
            DATA[self.columnName['8'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int )", i, 7)
            DATA[self.columnName['9'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int )", i, 8)
            DATA[self.columnName['10'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 9)
            DATA[self.columnName['11'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 10)
            DATA[self.columnName['12'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 11)
            DATA[self.columnName['13'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 12)
            DATA[self.columnName['14'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 13)
            DATA[self.columnName['15'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 14)
            DATA[self.columnName['16'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 15)
            DATA[self.columnName['17'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 16)
            DATA[self.columnName['18'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 17)
            DATA[self.columnName['19'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 18)
            DATA[self.columnName['20'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 19)
            DATA[self.columnName['21'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 20)
            DATA[self.columnName['22'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 21)
            DATA[self.columnName['23'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 22)
            DATA[self.columnName['24'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 23)
            DATA[self.columnName['25'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 24)
            DATA[self.columnName['26'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 25)
            DATA[self.columnName['27'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 26)
            DATA[self.columnName['28'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 27)
            DATA[self.columnName['29'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 28)
            DATA[self.columnName['30'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 29)
            DATA[self.columnName['31'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 30)
            DATA[self.columnName['32'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 31)
            DATA[self.columnName['33'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 32)
            DATA[self.columnName['34'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 33)
            DATA[self.columnName['35'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 34)
            DATA[self.columnName['36'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 35)
            DATA[self.columnName['37'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 36)
            DATA[self.columnName['38'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 37)
            DATA[self.columnName['39'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 38)
            DATA[self.columnName['40'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 39)
            DATA[self.columnName['41'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 40)
            DATA[self.columnName['42'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 41)
            DATA[self.columnName['43'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 42)
            DATA[self.columnName['44'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 43)
            DATA[self.columnName['45'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 44)
            DATA[self.columnName['46'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 45)
            DATA[self.columnName['47'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 46)
            DATA[self.columnName['48'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 47)
            DATA[self.columnName['49'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 48)
            DATA[self.columnName['50'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 49)
            DATA[self.columnName['51'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 50)
            DATA[self.columnName['52'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 51)
            DATA[self.columnName['53'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 52)
            DATA[self.columnName['54'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 53)
            DATA[self.columnName['55'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 54)
            DATA[self.columnName['56'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 55)
            DATA[self.columnName['57'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 56)
            DATA[self.columnName['58'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 57)
            DATA[self.columnName['59'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 58)
            DATA[self.columnName['60'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 59)
            DATA[self.columnName['61'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 60)
            DATA[self.columnName['62'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 61)
            DATA[self.columnName['63'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 62)
            DATA[self.columnName['64'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 63)
            DATA[self.columnName['65'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 64)
            DATA[self.columnName['66'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 65)
            DATA[self.columnName['67'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 66)
            DATA[self.columnName['68'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 67)
            DATA[self.columnName['69'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 68)
            DATA[self.columnName['70'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 69)
            DATA[self.columnName['71'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 70)
            DATA[self.columnName['72'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 71)
            DATA[self.columnName['73'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 72)
            DATA[self.columnName['74'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 73)
            DATA[self.columnName['75'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 74)
            DATA[self.columnName['76'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 75)
            DATA[self.columnName['77'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 76)
            DATA[self.columnName['78'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 77)
            DATA[self.columnName['79'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 78)
            DATA[self.columnName['80'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 79)
            DATA[self.columnName['81'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 80)
            DATA[self.columnName['82'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 81)
            DATA[self.columnName['83'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 82)
            DATA[self.columnName['84'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 83)
            DATA[self.columnName['85'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 84)
            DATA[self.columnName['86'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 85)
            DATA[self.columnName['87'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 86)
            DATA[self.columnName['88'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 87)
            DATA[self.columnName['89'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 88)
            DATA[self.columnName['90'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 89)
            DATA[self.columnName['91'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 90)
            DATA[self.columnName['92'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 91)
            DATA[self.columnName['93'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 92)
            DATA[self.columnName['94'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 93)'''
            DATA[self.columnName['1'].strip()] = self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 0)
            DATA[self.columnName['11'].strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 10)) # 개인 순매수
            DATA[self.columnName['17'].strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 16)) # 외국인 순매수
            DATA[self.columnName['23'].strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 22)) #기관순매수
            DATA[self.columnName['83'].strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 82)) #프로그램 순매수
            DATA[self.columnName['89'].strip()] = int(self.IndiTR.dynamicCall("GetMultiData(int, int)", i, 88)) #사모펀드 순매수

            DATA['stock_code'] = self.stock_code # 주식코드
            DATA['gubun'] = self.gubun # 주식코드
            DATA['gubun_code'] = self.gubun_code # 주식코드
            DATA['korName'] = self.korName # 주식코드

            DATA['start_date'] = self.start_date # 시작일
            DATA['end_date'] = self.end_date  # 마지막일
            DATA['연속일자'] = self.standard_length

            print("개인순매수")
            print(int(DATA[self.columnName['11'].strip()]))
            print("외국인 순매수 ")
            print(int(DATA[self.columnName['17'].strip()]))
            print("기관 순매수 ")
            print(int(DATA[self.columnName['23'].strip()] ))
            print("프로그램 순매수 ")
            print(int(DATA[self.columnName['83'].strip()]))
            if DATA[self.columnName['11'].strip()] is not '' and DATA[self.columnName['17'].strip()] is not '' and DATA[self.columnName['23'].strip()] is not '' and DATA[self.columnName['83'].strip()] is not '' :
                if int(DATA[self.columnName['11'].strip()])<0 and int(DATA[self.columnName['17'].strip()])>0 and int( DATA[self.columnName['83'].strip()] )>0:
                    check +=1
                    print("통과")
                else:
                    print("실패")
                    return

            else:
                return
        print("check")
        print(check)
        print("self.standard_length+1")
        print(self.standard_length)
        if check == self.standard_length+1:
            print("최종 통과")
            new_DATA = {

            }
            new_DATA['stock_code'] = DATA['stock_code']
            new_DATA['gubun'] =DATA['gubun']
            new_DATA['gubun_code'] = DATA['gubun_code']
            new_DATA['korName'] =DATA['korName']
            new_DATA['연속일자'] =DATA['연속일자']
            if self.collection1.find_one({'stock_code': new_DATA['stock_code']}):
                data_input = self.collection1.find_one({'stock_code': new_DATA['stock_code']}).copy()
                new_DATA['_id'] = data_input['_id']
                self.collection1.replace_one(data_input ,new_DATA, upsert=True)
            else:
                self.collection1.insert_one(new_DATA)

            #time.sleep(0.3)
            return

    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    db_name = sys.argv[1]
    client = MongoClient('127.0.0.1', 27017)
    db = client[db_name]
    collection_data = []
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
    end_date= get_endDay(sys.argv[1])
    for i in collection_data:
        standard_length = 0
        index = 0
        if checkindex == len(collection_data):
            TR_1206Event.exit(0)
            break
        while standard_length <= 2:
            start_date = end_date - timedelta(days=index)
            while True:
                if pytimekr.is_red_day(start_date):
                    index +=1
                    start_date = end_date - timedelta(days=index)
                else:
                    break
            start_date = str(start_date.strftime("%Y%m%d"))
            new_end_date = str(end_date.strftime("%Y%m%d"))
            TR_1206Event_vari = TR_1206(i['단축코드'], start_date, new_end_date, '1', '0', i['종목명'], i['구분'], i['구분코드'],
                                        db_name, standard_length)
            time.sleep(0.3)
            standard_length += 1
            index += 1
        checkindex += 1
    if checkindex != len(collection_data):
        TR_1206Event.exec_()

