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



class monitoring2():
    def __init__(self):
        self.timeline = common_min_timeline(5).timeline
        db_name = str(datetime.today().strftime("%Y%m%d"))
        #db_name = "20200206"
        collection_name1 = db_name+"_pr_input"
        collection_name2 = "SP_"+db_name
        collection_name3 = "SK_"+db_name
        client = MongoClient('127.0.0.1', 27017)
        db = client[db_name]
        collection1 = db[collection_name1]
        collection2 = db[collection_name2]
        collection3 = db[collection_name3]

        map_name = ""
        data_map ={

        }
        data_list1 = {}
        self.sorted_data_list1 = {}
        data_list2 = {}
        self.sorted_data_list2 = {}
        self.check_list = []
        self.final_data={

        }
        self.final_data2 = {

        }
        for i in collection1.find():
            if i['종목코드'] not in self.check_list:
                self.check_list.append(i['종목코드'])
                map_name = i['종목코드']
                self.final_data[map_name]={
                    "korName": i["korName"],
                    "gubun": i["gubun"]
                }
                self.final_data2[map_name]={
                    "korName": i["korName"],
                    "gubun": i["gubun"]
                }
            else:
                continue
            data_list1[map_name]= []
            self.sorted_data_list1[map_name]= []
            for j in collection2.find({'단축코드': map_name}):
                j['시간']= int(j['시간'])
                data_list1[map_name].append(j)
                print(j)
            self.sorted_data_list1[map_name] = sorted(data_list1[map_name], key = lambda  x: x['시간'])

            data_list2[map_name]= []
            self.sorted_data_list2[map_name]= []
            for j in collection3.find({'단축코드': map_name}):
                j['시간']= int(j['시간'])
                j['외국계순매수수량']= int(j['외국계순매수수량'])
                data_list2[map_name].append(j)
                print(j)
            self.sorted_data_list2[map_name] = sorted(data_list2[map_name], key = lambda  x: x['시간'])
            map_name = ""
    def preprocessProgram(self):
        for i in self.check_list:
            self.final_data[i]['프로그램'] = []
            data_list1 = self.sorted_data_list1[i]
            x_value = [d['시간'] for d in data_list1]
            y_value = [d['비차익매수위탁체결수량'] - d['비차익매도위탁체결수량'] for d in data_list1]
            print(x_value)
            print(y_value)
            indexcheck = 0
            standard_length = len(self.timeline)
            real_time_length = len(x_value)
            for j in range(standard_length):
                self.final_data[i]['프로그램'].append(0)
            for j in range(standard_length):
                print(i)
                index = indexcheck
                if index == real_time_length:
                    self.final_data[i]['프로그램'][j] = self.final_data[i]['프로그램'][j - 1]
                    continue
                for k in range(index, real_time_length):
                    if j == standard_length - 1:
                        self.final_data[i]['프로그램'][j] = self.final_data[i]['프로그램'][j - 1]
                        break
                    elif (int)(self.timeline[j]) < (int)(x_value[k]) and (int)(x_value[k]) <= (int)(self.timeline[j + 1]):
                        self.final_data[i]['프로그램'][j + 1] = (int)(y_value[k])
                        indexcheck += 1
                    elif (int)(self.timeline[j]) == (int)(x_value[k]):
                        self.final_data[i]['프로그램'][j] = (int)(y_value[k])
                        indexcheck += 1
                        break
                    elif (int)(x_value[k]) < (int)(self.timeline[j]):
                        indexcheck += 1
                        continue
                    else:
                        if j == 0:
                            break
                        else:
                            if self.final_data[i]['프로그램'][j] == 0:
                                self.final_data[i]['프로그램'][j] = self.final_data[i]['프로그램'][j - 1]
                                break
                            else:
                                break
            print(self.final_data)
    def preprocessForeign(self):
        for i in self.check_list:
            self.final_data2[i]['외국계순매수수량']=[]
            data_list2 = self.sorted_data_list2[i]
            x_value2 = [d['시간'] for d in data_list2]
            y_value2 = [d['외국계순매수수량'] for d in data_list2]
            indexcheck = 0
            standard_length = len(self.timeline)
            real_time_length = len(x_value2)
            for j in range(standard_length):
                self.final_data2[i]['외국계순매수수량'].append(0)
            for j in range(standard_length):
                print(i)
                index = indexcheck
                if index == real_time_length:
                    self.final_data2[i]['외국계순매수수량'][j] = self.final_data2[i]['외국계순매수수량'][j - 1]
                    continue
                for k in range(index, real_time_length):
                    if j == standard_length - 1:
                        self.final_data2[i]['외국계순매수수량'][j] = self.final_data2[i]['외국계순매수수량'][j - 1]
                        break
                    elif (int)(self.timeline[j]) < (int)(x_value2[k]) and (int)(x_value2[k]) <= (int)(self.timeline[j + 1]):
                        self.final_data2[i]['외국계순매수수량'][j + 1] = (int)(y_value2[k])
                        indexcheck += 1
                    elif (int)(self.timeline[j]) == (int)(x_value2[k]):
                        self.final_data2[i]['외국계순매수수량'][j] = (int)(y_value2[k])
                        indexcheck += 1
                        break
                    elif (int)(x_value2[k]) < (int)(self.timeline[j]):
                        indexcheck += 1
                        continue
                    else:
                        if j == 0:
                            break
                        else:
                            if self.final_data2[i]['외국계순매수수량'][j] == 0:
                                self.final_data2[i]['외국계순매수수량'][j] = self.final_data2[i]['외국계순매수수량'][j - 1]
                                break
                            else:
                                break
            print(self.final_data2)


if __name__ == "__main__":
    monitoring2_var = monitoring2()
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



