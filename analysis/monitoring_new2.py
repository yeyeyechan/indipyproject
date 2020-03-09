# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")
from pymongo import MongoClient
import datetime

from analysis.common_data import common_min_timeline
from analysis.common_data import common_min_shortTime
from log.logger_pyflask import logging_instance
import pymongo


class monitoring_new2():
    def __init__(self, date):
        self.realTimeLogger = logging_instance("monitoring_new2.py_").mylogger
        self.timeline = common_min_timeline(5).timeline
        self.shortTimeline = common_min_shortTime(5).timeline
        self.date = date
        self.shortTimeRightNow =""
        db_name = self.date

        collection_name1 = db_name+"_pr_input"
        collection_name2 = "SP_5min_"+db_name
        collection_name3 = "SK_5min_"+db_name
        collection_name4 = "SC_5min_"+db_name
        self.realTimeLogger.info("collection 생성 전")
        client = MongoClient('127.0.0.1', 27017)
        db = client[db_name]
        collection1 = db[collection_name1] #인풋 컬렉션
        collection2 = db[collection_name2] #프로그램 매수 매도 컬렉션
        collection3 = db[collection_name3] #외국인 매수 매도 컬렉션
        collection4 = db[collection_name4] #현재가  컬렉션
        self.realTimeLogger.info("collection 생성 후")

        self.acc_stock_code = {

        }

        map_name = ""
        data_map ={

        }
        data_list1 = {}
        self.sorted_data_list1 = {}

        data_list2 = {}
        self.sorted_data_list2 = {}

        data_list3 = {}
        self.sorted_data_list3 = {}

        self.check_list = []

        self.final_data={

        }
        self.final_data2 = {

        }
        self.final_data3 = {

        }

        for i in collection1.find():
            if i['종목코드'] not in self.check_list:

                self.check_list.append(i['종목코드'])
                self.realTimeLogger.info("종목코드 추가    "+i['종목코드'])
                map_name = i['종목코드']
                self.final_data[map_name]={
                    "korName": i["korName"],
                    "gubun": i["gubun"],
                    "프로그램":[]
                }
                self.final_data2[map_name]={
                    "korName": i["korName"],
                    "gubun": i["gubun"],
                    "외국계순매수수량": [],
                    '연속일자':0

                }
                self.final_data3[map_name]={
                    "korName": i["korName"],
                    "gubun": i["gubun"],
                    "종가":[]
                }
                self.realTimeLogger.info("collection4 에서 확인해  Trading_Value 를 acc_stock_code 추가   전 ")

                if collection4.find_one({"stock_code": i['종목코드']}):
                    self.realTimeLogger.info("collection4 에 종목코드  "+i['종목코드'] +" 존재")
                    for collection4_input in collection4.find({"stock_code": i['종목코드']}).sort([("SortTime", pymongo.DESCENDING)]):
                        self.realTimeLogger.info("collection4 Trading Value 로 sort 해서 acc_stock_code에 넣기 "+ i['종목코드'])
                        self.acc_stock_code[i['종목코드']] = collection4_input['Trading_Value']
                        break
                    self.realTimeLogger.info("collection4 Trading Value 로 sort 해서 acc_stock_code에 넣기 완료 "+ i['종목코드'])
                else:
                    self.acc_stock_code[i['종목코드']] = 0
                self.realTimeLogger.info("collection4 에서 확인해  Trading_Value 를 acc_stock_code 추가   후 ")

            else:
                continue

            data_list1[map_name]= []
            self.sorted_data_list1[map_name]= []
            self.realTimeLogger.info("collection2 에서 확인해  프로그램 매수 데이터 DATA_list1 에 넣기 전 ")
            for j in collection2.find({'단축코드': map_name}):
                j['시간']= int(j['시간'])
                data_list1[map_name].append(j)
            self.realTimeLogger.info("collection2 에서 확인해  프로그램 매수 데이터 DATA_list1 에 넣기 완료 ")
            self.realTimeLogger.info("data_list1 sort 해서 sorted_data_list1에 넣어 주기 전 ")
            self.sorted_data_list1[map_name]= sorted(data_list1[map_name], key = lambda  x: x['시간'])
            self.realTimeLogger.info("data_list1 sort 해서 sorted_data_list1에 넣어 주기 완료 ")

            for j in range(78):
                self.final_data[i['종목코드']]['프로그램'].append(0)
            index1 = 0
            self.realTimeLogger.info("sorted_data_list1 에서 final_data 에 넣기 전 ")
            for sorted_data in self.sorted_data_list1[map_name]:
                while True:
                    if (int)(self.shortTimeline[index1] )== sorted_data['시간']:
                        self.realTimeLogger.info("프로그램 매수 계산하여 final_data에 직접넣기 전")
                        self.final_data[map_name]['프로그램'][index1] = (sorted_data['비차익매수위탁체결수량']-sorted_data['비차익매도위탁체결수량'])
                        self.realTimeLogger.info("프로그램 매수 계산하여 final_data에 직접넣기 후")
                        break
                    else:
                        pass
                    index1 +=1
            self.realTimeLogger.info("sorted_data_list1 에서 final_data 에 넣기 완료")


            data_list2[map_name]= []
            self.sorted_data_list2[map_name]= []
            self.realTimeLogger.info("collection3 외국계 순매수 수량 데이터 data_list2로 저장 전")
            for j in collection3.find({'단축코드': map_name}):
                j['시간']= int(j['시간'])
                j['외국계순매수수량']= int(j['외국계순매수수량'])
                j['연속일자'] = i['연속일자']
                data_list2[map_name].append(j)
            self.realTimeLogger.info("collection3 외국계 순매수 수량 데이터 data_list2로 저장 후")

            self.sorted_data_list2[map_name]=  sorted(data_list2[map_name], key = lambda  x: x['시간'])
            for j in range(78):
                self.final_data2[i['종목코드']]['외국계순매수수량'].append(0)
            index2 = 0
            for sorted_data in self.sorted_data_list2[map_name]:
                while True:
                    if (int)(self.shortTimeline[index2] )== sorted_data['시간']:
                        self.realTimeLogger.info("final_data2 에 외국계 순매수 수량 데이터 저장 전")
                        self.final_data2[map_name]['외국계순매수수량'][index2] = (sorted_data['외국계순매수수량'])
                        self.realTimeLogger.info("final_data2 에 외국계 순매수 수량 데이터 저장 후")

                        print(sorted_data)
                        break
                    else:
                        pass
                    index2 +=1
            self.realTimeLogger.info("final_data2 에 외국계 순매수 수량 데이터 저장 완료")
            print(self.final_data2[map_name]['연속일자'])
            print(self.sorted_data_list2[map_name])
            if len(self.sorted_data_list2[map_name]) == 0 :
                self.realTimeLogger.info("sorted_data_list2 비어있음 종목코드 : "+map_name)
                self.realTimeLogger.info("처음으로 되돌아감")
                continue
            print((int)(self.sorted_data_list2[map_name][0]['연속일자']) +1)
            self.final_data2[map_name]['연속일자'] = (int)(self.sorted_data_list2[map_name][0]['연속일자']) +1

            data_list3[map_name]= []
            self.sorted_data_list3[map_name]= []
            self.realTimeLogger.info("collection4 에서 종가 데이터 확인하여 data_list3에 넣기")
            for j in collection4.find({'stock_code': map_name, 'DATE':db_name }):
                j['시간']= int(j['TIME'])
                j['종가']= int(j['Close'])
                data_list3[map_name].append(j)
            self.realTimeLogger.info("collection4 에서 종가 데이터 확인하여 data_list3에 넣기 완료")

            self.sorted_data_list3[map_name] = sorted(data_list3[map_name], key = lambda  x: x['시간'])
            for j in range(78):
                self.final_data3[i['종목코드']]['종가'].append(0)
            index3 = 0
            self.realTimeLogger.info("sorted_data_list3 에서 종가 데이터 확인하여 final_data3 넣기 전")
            for sorted_data in self.sorted_data_list3[map_name]:
                while True:
                    if (int)(self.shortTimeline[index3] )== sorted_data['시간']:
                        self.final_data3[map_name]['종가'][index3] = (sorted_data['종가'])
                        break
                    else:
                        pass
                    index3 +=1
            self.realTimeLogger.info("sorted_data_list3 에서 종가 데이터 확인하여 final_data3 넣기 완료")
        # check_list 안의 종목코드를 가지고 검색하여 외국인 순매수 >0 인 종목코드만 검색한다.
        self.realTimeLogger.info("check_list 안의 종목코드를 가지고 검색하여 외국인 순매수 >0 인 종목코드만 검색한다.")
        self.realTimeLogger.info("self.check_list" )
        self.realTimeLogger.info(self.check_list)
        self.shortTimeRightNow = datetime.datetime.now()
        self.hour = self.shortTimeRightNow.hour
        self.min = self.shortTimeRightNow.minute
        self.shortTimeRightNow = self.hour*100 +self.min
        index = 0
        for timecheck in self.shortTimeline:
            if (int)(timecheck) >= self.shortTimeRightNow:
                break
            index +=1

        for check_input in self.check_list:
            if self.final_data2[check_input]['외국계순매수수량'][index] <=0 :
                print(index)
                print(self.final_data2[check_input]['외국계순매수수량'][index])
                print(self.final_data2[check_input]['외국계순매수수량'])
                self.realTimeLogger.info(" self.acc_stock_code['check_input'] 제거  ")
                del self.acc_stock_code[check_input]
        self.realTimeLogger.info("제거 작업후 acc_stock_code 딕셔너리 sort ")
        self.acc_stock_code = sorted( self.acc_stock_code.items() , key = (lambda  x: x[1]), reverse = True )
        self.realTimeLogger.info("self.acc_stock_code" )
        self.realTimeLogger.info(self.acc_stock_code)


if __name__ == "__main__":
    monitoring2_var = monitoring_new2("20200303")





