# -*- coding: utf-8 -*-
import sys
from pandas import Series, DataFrame
import pandas as pd
from time import sleep
import threading
import numpy as np
from pymongo import MongoClient
from data.common import  weekday_check
from datetime import timedelta, datetime
from data.common import mongo_find
from analysis.common_data import common_min_timeline
from log.logger_pyflask import logging_instance



class monitoring_new():
    def __init__(self, date):
        self.realTimeLogger = logging_instance("monitoring_new.py_").mylogger

        self.timeline = common_min_timeline(5).timeline
        self.date = date
        db_name = self.date

        collection_name1 = db_name+"_pr_input"
        collection_name2 = "SP_5min_"+db_name
        collection_name3 = "SK_5min_"+db_name
        collection_name4 = "TR_SCHART_5min_"+db_name

        client = MongoClient('127.0.0.1', 27017)

        db = client[db_name]
        collection1 = db[collection_name1] #인풋 컬렉션
        collection2 = db[collection_name2] #프로그램 매수 매도 컬렉션
        collection3 = db[collection_name3] #외국인 매수 매도 컬렉션
        collection4 = db[collection_name4] #현재가  컬렉션

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
                map_name = i['종목코드']
                self.final_data[map_name]={
                    "korName": i["korName"],
                    "gubun": i["gubun"],
                    "프로그램":[]
                }
                self.final_data2[map_name]={
                    "korName": i["korName"],
                    "gubun": i["gubun"],
                    "외국계순매수수량": []

                }
                self.final_data3[map_name]={
                    "korName": i["korName"],
                    "gubun": i["gubun"],
                    "종가":[]
                }
            else:
                continue

            data_list1[map_name]= []
            self.sorted_data_list1[map_name]= []

            for j in collection2.find({'단축코드': map_name}):
                j['시간']= int(j['시간'])
                data_list1[map_name].append(j)

            self.sorted_data_list1[map_name]= sorted(data_list1[map_name], key = lambda  x: x['시간'])
            for j in range(78):
                self.final_data[i['종목코드']]['프로그램'].append(0)
            index1 = 0
            for sorted_data in self.sorted_data_list1[map_name]:
                self.final_data[map_name]['프로그램'][index1] = (sorted_data['비차익매수위탁체결수량']-sorted_data['비차익매도위탁체결수량'])
                index1 +=1


            data_list2[map_name]= []
            self.sorted_data_list2[map_name]= []

            for j in collection3.find({'단축코드': map_name}):
                j['시간']= int(j['시간'])
                j['외국계순매수수량']= int(j['외국계순매수수량'])
                data_list2[map_name].append(j)

            self.sorted_data_list2[map_name]=  sorted(data_list2[map_name], key = lambda  x: x['시간'])
            for j in range(78):
                self.final_data2[i['종목코드']]['외국계순매수수량'].append(0)
            index2 = 0
            for sorted_data in self.sorted_data_list2[map_name]:
                self.final_data2[map_name]['외국계순매수수량'][index2] = (sorted_data['외국계순매수수량'])
                index2 +=1

            data_list3[map_name]= []
            self.sorted_data_list3[map_name]= []

            for j in collection4.find({'stock_code': map_name, 'DATE':db_name }):
                j['시간']= int(j['TIME'])
                j['종가']= int(j['Close'])
                data_list3[map_name].append(j)

            self.sorted_data_list3[map_name] = sorted(data_list3[map_name], key = lambda  x: x['시간'])
            for j in range(78):
                self.final_data3[i['종목코드']]['종가'].append(0)
            index3 = 0
            for sorted_data in self.sorted_data_list3[map_name]:
                self.final_data3[map_name]['종가'][index3] = (sorted_data['종가'])
                index3 +=1

            self.realTimeLogger.info("sorted")

            map_name = ""

if __name__ == "__main__":
    monitoring2_var = monitoring_new()
    monitoring2_var.preprocess()
    print(monitoring2_var.final_data)
    '''data_list = monitoring_var.sorted_data_list['012800']
    x_value = [d['시간'] for d in  data_list ]
    y_value = [d['비차익매수위탁체결수량']- d['비차익매도위탁체결수량'] for d in  data_list]
    time_line =[]
    input = 90000
    y_real = []
    x_index =0
    y_index =0
    y_real.append(0)
    check =False
    time_line.append(str(input))
    while True:
        hour =int(input/10000)
        min = (int)((input%10000))
        if min == 0:
            pass
        else:
            min = (int)(min/100)
        next_input = hour*60+min+5
        next_input = (int)((int)(next_input/60)*10000)+(int)(next_input%60*100)


        while True:
            if x_value[x_index]<next_input:
                y_real[y_index] =y_value[x_index]
                x_index +=1
                if x_index == len(x_value):
                    while True:
                        if input == 154000:
                            check = True
                            break
                        else:
                            time_line.append(str(input))
                            y_real.append(y_real[y_index - 1])
                            hour = int(input / 10000)
                            min = (int)((input % 10000))
                            if min == 0:
                                pass
                            else:
                                min = (int)(min / 100)
                            input = hour * 60 + min + 5
                            input = (int)((int)(input / 60) * 10000) + (int)(input % 60 * 100)
                    if check:
                        break
            else:
                break
        if check:
            break
        input = next_input
        y_index +=1
        y_real.append(y_real[y_index-1])
        time_line.append(str(input))
        print("time_line current")
        print(time_line[y_index-1])
        print("y_value current")
        print(y_real[y_index-1])'''



