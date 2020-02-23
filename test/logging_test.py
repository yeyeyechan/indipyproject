import logging
import logging.config
import json
import os
if __name__ == '__main__':
    print(os.getcwd())
    with open('../pyflask/log/logging.json','rt', encoding='UTF8') as f :
        config = json.load(f)
    print(config)
    logging.config.dictConfig(config)
    mylogger = logging.getLogger("pyflask")
    stream_handler  = logging.StreamHandler()
    mylogger.addHandler(stream_handler)
    logging.info("sever start")

    '''formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler  = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    mylogger.addHandler(stream_handler)

    file_handler = logging.FileHandler('my.log')
    file_handler.setFormatter(formatter)
    mylogger.addHandler(file_handler)

    logging.error("sever start")'''

