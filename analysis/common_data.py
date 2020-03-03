
import datetime
from datetime import timedelta
from pytimekr import pytimekr
class common_min_timeline():
    def __init__(self, standard):
        #standard 기준이 되는 int값
        self.timeline = []
        self.standard = standard
        input =90500
        self.timeline.append((str)(input))
        while True:
            hour = (int)(input / 10000)
            min = (int)(input % 10000)
            if min == 0:
                pass
            else:
                min = (int)(min / 100)
            next_input = hour * 60 + min + self.standard
            next_input = (int)(next_input / 60) * 10000 + (int)(next_input % 60 * 100)
            self.timeline.append((str)(next_input))
            if input >152500:
                break
            else:
                input = next_input
        print(self.timeline)
class common_min_shortTime():
    def __init__(self, standard):
        #standard 기준이 되는 int값
        self.timeline = []
        self.standard = standard
        input =905

        self.timeline.append("0905")
        while True:
            hour = (int)(input / 100)
            min = (int)(input % 100)
            if min == 0:
                pass
            else:
                min = (int)(min)
            next_input = hour * 60 + min + self.standard
            next_input = (int)(next_input / 60) * 100 + (int)(next_input % 60)
            if (int)(next_input/100) == 9:
                self.timeline.append("0"+(str)(next_input))
            else:
                self.timeline.append((str)(next_input))
            if input >1520:
                break
            else:
                input = next_input
        print(self.timeline)
        print(len(self.timeline))
def get_endDay(db_name):
    index = 1
    end_date = datetime.datetime.strptime(db_name, '%Y%m%d') - timedelta(days=index)
    if pytimekr.is_red_day(end_date):
        while True:
            index +=1
            end_date = datetime.datetime.strptime(db_name, '%Y%m%d') - timedelta(days=index)
            if pytimekr.is_red_day(end_date):
                continue
            else:
                break
    return end_date
if __name__ == "__main__":
    print(get_endDay("20200302"))
