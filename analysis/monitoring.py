# -*- coding: utf-8 -*-

from pymongo import MongoClient
from datetime import datetime

from analysis.common_data import common_min_timeline


class monitoring():
    def __init__(self):
        print("test")
        self.timeline = common_min_timeline(5).timeline

        db_name = str(datetime.today().strftime("%Y%m%d"))
        #db_name = "20200206"
        print(db_name)
        collection_name1 = db_name+"_pr_input"
        collection_name2 = "SP_"+db_name
        client = MongoClient('127.0.0.1', 27017)

        db = client[db_name]
        collection1 = db[collection_name1]
        collection2 = db[collection_name2]

        map_name = ""
        data_map ={

        }
        data_list = {}
        self.sorted_data_list = {}
        self.check_list = []
        self.final_data={

        }

        for i in collection1.find():
            if i['종목코드'] not in self.check_list:
                self.check_list.append(i['종목코드'])
                map_name = i['종목코드']
                self.final_data[map_name]={

                }

            else:
                continue
            data_list[map_name]= []
            self.sorted_data_list[map_name]= []
            for j in collection2.find({'단축코드': map_name}):
                j['시간']= int(j['시간'])
                data_list[map_name].append(j)
                print(j)
            self.sorted_data_list[map_name] = sorted(data_list[map_name], key = lambda  x: x['시간'])
            map_name = ""
        print("Test1")

    def preprocess(self):
        for i in self.check_list:
            self.final_data[i]['프로그램']=[]
            data_list = self.sorted_data_list[i]
            x_value = [d['시간'] for d in data_list]
            y_value = [d['비차익매수위탁체결수량'] - d['비차익매도위탁체결수량'] for d in data_list]
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
                    if j == standard_length-1:
                        self.final_data[i]['프로그램'][j] = self.final_data[i]['프로그램'][j - 1]
                        break
                    elif (int)(self.timeline[j]) < (int)(x_value[k]) and (int)(x_value[k]) <=(int)(self.timeline[j+1]):
                        self.final_data[i]['프로그램'][j+1] = (int)(y_value[k])
                        indexcheck +=1
                    elif (int)(self.timeline[j])  ==   (int)(x_value[k]) :
                        self.final_data[i]['프로그램'][j] = (int)(y_value[k])
                        indexcheck +=1
                        break
                    elif   (int)(x_value[k])  < (int)(self.timeline[j]) :
                        indexcheck += 1
                        continue
                    else:
                        if j == 0:
                            break
                        else:
                            if self.final_data[i]['프로그램'][j] == 0:
                                self.final_data[i]['프로그램'][j] = self.final_data[i]['프로그램'][j-1]
                                break
                            else:
                                break
            print(self.final_data)



'''            time_line = []
            input = 90000
            y_real = []
            x_index = 0
            y_index = 0
            y_real.append(0)
            check = False
            time_line.append(str(input))
            while True:
                hour = int(input / 10000)
                min = (int)((input % 10000))
                if min == 0:
                    pass
                else:
                    min = (int)(min / 100)
                next_input = hour * 60 + min + 5
                next_input = (int)((int)(next_input / 60) * 10000) + (int)(next_input % 60 * 100)

                while True:
                    if input < x_value[x_index] and x_value[x_index] <=next_input:
                        y_real[y_index] = y_value[x_index]
                        x_index += 1
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
                y_index += 1
                y_real.append(y_real[y_index - 1])
                time_line.append(str(input))
                print("time_line current")
                print(time_line[y_index - 1])
                print("y_value current")
                print(y_real[y_index - 1])

                self.final_data[i]['시간'] = time_line.copy()
                self.final_data[i]['프로그램'] = y_real.copy()'''

if __name__ == "__main__":
    monitoring_var = monitoring()
    monitoring_var.preprocess()
    print(monitoring_var.final_data)




