
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
def make_five_min(time):
    final_time = 0
    final_hour = 0
    final_min = 0
    # time is HHMMSSSS
    if len(time) ==8 or len(time) ==7 :
        hour = (int)((int)(time)/ 1000000)
        min_ss = (int)((int)(time)% 1000000)
        min = (int)(min_ss/10000)
        ss  = min_ss%10000

        if min%5 ==0 and ss ==0:
            final_min = min
            final_hour = hour
        else:
            if min >=55:
                final_hour = hour +1
                final_min =0
            else:
                final_hour = hour
                final_min = 5*(int)(min/5) +5
    elif len(time) ==4 or len(time) ==3 :
        hour = (int)((int)(time) / 100)
        min  = (int)((int)(time) % 100)

        if min % 5 == 0 :
            final_min = min
            final_hour = hour
        else:
            if min >= 55:
                final_hour = hour + 1
                final_min = 0
            else:
                final_hour = hour
                final_min =  5*(int)(min/5) + 5

    final_time = final_hour*100 +final_min
    if final_hour <10:
        final_time = "0"+str(final_time)
    return str(final_time)

if __name__ =="__main__":
    print(make_five_min("759"))
