from matplotlib import pyplot as plt
from matplotlib import rc
import numpy
import matplotlib
import matplotlib.font_manager  as fm
from matplotlib import rc
from data.common import mongo_find
from pymongo import MongoClient


class makeChart :
    def __init__(self, collection_name, x,y, font):
        self.x = x
        self.y = y
        self.collection_name = collection_name
        self.font = font
    def drawBarChart (self):
        matplotlib.rc('font', family= self.font)
        plt.plot(self.x,self.y)
        plt.xlabel(self.collection_name)
        plt.ylabel("거래량")
        plt.show()
        plt.savefig(self.collection_name, dpi = 300)
        return






if __name__ == "__main__":
    font_path = "C:/Windows/Fonts/malgun.ttf"
    fontprop = fm.FontProperties(fname= font_path, size = 18)
    fontname = fm.FontProperties(fname= font_path, size = 18).get_name()
    chart_name = "TR_1205_3"

    client = MongoClient('127.0.0.1', 27017)
    db = client["stock_data"]
    collection = db[chart_name]
    x = []
    y = []
    for i in collection.find().sort("외국인순매수", -1):
        if i['개인순매수']<0 and i['외국인순매수']>0 :
            x.append(i['한글업종명'])
            y.append(i['외국인순매수'])

    chart_vari = makeChart(chart_name, x,y, fontname)
    chart_vari.drawBarChart()

    '''font_path = "C:/Windows/Fonts/malgun.ttf"
    fontprop = fm.FontProperties(fname= font_path, size = 18)
    fontname = fm.FontProperties(fname= font_path, size = 18).get_name()
    chart_name = "TR_1864_20200117"

    client = MongoClient('127.0.0.1', 27017)
    db = client["stock_data"]
    collection = db[chart_name]
    x = []
    y = []
    for i in collection.find().sort("외국인순매수", -1):
        if i['개인순매수']<0 and i['외국인순매수']>0 :
            x.append(i['한글업종명'])
            y.append(i['외국인순매수'])

    chart_vari = makeChart(chart_name, x,y, fontname)
    chart_vari.drawBarChart()'''