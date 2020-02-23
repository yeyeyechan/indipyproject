import logging.config
import json
import datetime
import os
import sys
class logging_instance:
    def __init__(self, name):
        #os.path.append("C:\\dev\\indiPyProject\\log")
        logging_file_name_prefix = str(datetime.datetime.today().strftime("%Y%m%d"))
        logging_file_name = "..\log\\"+ logging_file_name_prefix+"_app.log"
        with open('..\log\logging.json','rt', encoding='UTF8') as f :
            config = json.load(f)
        config['handlers']['info_file_handler']['filename'] =logging_file_name
        #config 설정 및 logger 만들기
        logging.config.dictConfig(config)
        self.mylogger = logging.getLogger(name+ str(datetime.datetime.now().time()))
if __name__ =="__main__":
    test = logging_instance("test")


