

# -*- coding: utf-8 -*-
import sys
import time
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from time import sleep
import requests
from pymongo import MongoClient
import datetime
from datetime import timedelta
from data.common import mongo_find
import json
class SB(QMainWindow):
    def __init__(self, stock_code):
        super().__init__()
        # 인디의 TR을 처리할 변수를 생성합니다.
        self.IndiTR = QAxWidget("GIEXPERTCONTROL.GiExpertControlCtrl.1")


        # Indi API event
        self.IndiTR.ReceiveData.connect(self.ReceiveData)
        self.IndiTR.ReceiveSysMsg.connect(self.ReceiveSysMsg)

        self.stock_code= stock_code

        self.btn_Search()

    # 그럼 실제로 과거 주가를 받아오는 부분은 다음과 같습니다.
    def btn_Search(self):

        # 차트조회 : 과거주가는 차트조회를 통해 받아올 수 있습니다.
        # TR_SCHART : 과거주가를 요청할 TR입니다.
        # 해당 TR의 필드입력형식에 맞춰서 TR을 날리면 됩니다.
        # 데이터 요청 형식
        ret = self.IndiTR.dynamicCall("SetQueryName(QString)", "SB")
        ret = self.IndiTR.dynamicCall("SetSingleData(int, QString)", 0, self.stock_code) # 단축코드
        rqid = self.IndiTR.dynamicCall("RequestData()") # 데이터 요청
    # 요청한 TR로 부터 데이터를 받는 함수입니다.
    def ReceiveData(self, rqid):
        # TR을 날릴때 ID를 통해 TR이름을 가져옵니다.
        # GetMultiRowCount()는 TR 결과값의 multi row 개수를 리턴합니다.
        column =['단축코드' , '업종한글명', '한글종목명', '업종코드']
        dict = {
            '0001': '종합주가지수(KOSPI)       ',
            '0002': '대형주                 ',
            '0003': '중형주                 ',
            '0004': '소형주                 ',
            '0005': '음식료품                ',
            '0006': '섬유,의복               ',
            '0007': '종이,목재               ',
            '0008': '화학                  ',
            '0009': '의약품                 ',
            '0010': '비금속광물               ',
            '0011': '철강및금속               ',
            '0012': '기계                  ',
            '0013': '전기,전자               ',
            '0014': '의료정밀                ',
            '0015': '운수장비                ',
            '0016': '유통업                 ',
            '0017': '전기가스업               ',
            '0018': '건설업                 ',
            '0019': '운수창고                ',
            '0020': '통신업                 ',
            '0021': '금융업                 ',
            '0022': '은행                  ',
            '0024': '증권                  ',
            '0025': '보험                  ',
            '0026': '서비스업                ',
            '0027': '제조업                 ',
            '1001': '종합지수                ',
            '1002': 'KOSDAQ 100          ',
            '1003': 'KOSDAQ MID 300      ',
            '1004': 'KOSDAQ SMALL        ',
            '1012': '기타서비스               ',
            '1015': 'KOSDAQIT종합          ',
            '1024': '제조                  ',
            '1026': '건설                  ',
            '1027': '유통                  ',
            '1029': '운송                  ',
            '1031': '금융                  ',
            '1037': '오락문화                ',
            '1041': '통신방송서비스             ',
            '1042': 'IT S/W & SVC        ',
            '1043': 'IT H/W              ',
            '1056': '음식료,담배              ',
            '1058': '섬유,의류               ',
            '1062': '종이,목재               ',
            '1063': '출판,매체복제             ',
            '1065': '화학                  ',
            '1066': '제약                  ',
            '1067': '비금속                 ',
            '1068': '금속                  ',
            '1070': '기계,장비               ',
            '1072': '일반전기전자              ',
            '1074': '의료,정밀기기             ',
            '1075': '운송장비,부품             ',
            '1077': '기타 제조               ',
            '1151': '통신서비스               ',
            '1152': '방송서비스               ',
            '1153': '인터넷                 ',
            '1154': '디지털컨텐츠              ',
            '1155': '소프트웨어               ',
            '1156': '컴퓨터서비스              ',
            '1157': '통신장비                ',
            '1158': '정보기기                ',
            '1159': '반도체                 ',
            '1160': 'IT부품                ',
            '1181': '코스닥 우량기업            ',
            '1182': '코스닥 벤처기업            ',
            '1183': '코스닥 중견기업            ',
            '1184': '코스닥 신성장기업           ',
            '1202': 'KOSDAQ 프리미어지수       ',
            '2101': 'KOSPI200 종합         ',
            '2121': 'KOSPI200 레버리지 지수    ',
            '2123': 'F-KOSPI200 지수       ',
            '2124': 'F-KOSPI200 인버스 지수   ',
            '2151': 'K200 건설기계           ',
            '2152': 'K200 조선운송           ',
            '2153': 'K200 철강소재           ',
            '2154': 'K200 에너지화학          ',
            '2155': 'K200 정보통신           ',
            '2156': 'K200 금융             ',
            '2157': 'K200 필수소비재          ',
            '2158': 'K200 자유소비재          ',
            '2201': 'KOSPI 100           ',
            '2202': 'KOSPI 50            ',
            '2300': '정보통신지수              ',
            '2400': 'KODI                ',
            '2401': 'K200 동일가중지수         ',
            '2402': 'K100 동일가중지수         ',
            '2403': 'K50 동일가중지수          ',
            '2500': 'KOGI                ',
            '2501': '사회책임투자지수            ',
            '2502': '환경책임투자지수            ',
            '2503': '녹색환경투자지수            ',
            '6103': 'KOSDAQ 스타지수         '}
        # 데이터 양식
        DATA = {}

        print(self.IndiTR.dynamicCall("GetSingleData(int)", 0) )
        # 데이터 받기
        DATA[column[0]] = self.IndiTR.dynamicCall("GetSingleData(int)", 1)  # 단축코드
        DATA[column[1]] = dict[self.IndiTR.dynamicCall("GetSingleData(int)", 2).strip() + self.IndiTR.dynamicCall("GetSingleData(int)", 8).strip()].strip()#장구분
        DATA[column[2]] = self.IndiTR.dynamicCall("GetSingleData(int)", 5).strip()  # 한글종목명
        DATA[column[3]] = self.IndiTR.dynamicCall("GetSingleData(int)", 2).strip() + self.IndiTR.dynamicCall("GetSingleData(int)", 8).strip()
        client = MongoClient('127.0.0.1', 27017)
        db = client["stock_data"]
        collection = db["SB_20200119"]
        collection.insert(DATA)
        print(DATA)
        sleep(0.05)
    # 시스템 메시지를 받은 경우 출력합니다.
    def ReceiveSysMsg(self, MsgID):
        print("System Message Received = ", MsgID)

if __name__ == "__main__":
    client = MongoClient('127.0.0.1', 27017)
    db = client["stock_data"]
    collection = db["TR_1864_20200117"]
    app = QApplication(sys.argv)
    for i in collection.find():
        if i['전일대비율']>3.0:
            SB_vari = SB(i['단축코드'])
    app.exec_()