from pymongo import MongoClient
import datetime
if __name__ =="__main__":
    db_name = datetime.datetime.today().strftime("%Y%m%d")
    collection_name = db_name + "_pr_input2"
    client = MongoClient('127.0.0.1', 27017)
    db = client[db_name]
    collection_input1 = "TR_1206_new2_" + db_name

    collection = db[collection_name]
    collection1 = db[collection_input1]
    for i in collection1.find():
        data = {
            "종목코드": i['stock_code'],
            "korName": i["korName"],
            "gubun": i["gubun"],
            "gubun_code": i["gubun_code"],
            "연속일자": i["연속일자"]

        }
        if collection.find_one({'종목코드': data['종목코드']}):
            data_input = collection.find_one({'종목코드': data['종목코드']}).copy()
            data['_id'] = data_input['_id']
            collection.replace_one(data_input, data, upsert=True)
        else:
            collection.insert_one(data)
