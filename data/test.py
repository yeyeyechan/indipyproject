from pymongo import MongoClient
from pytimekr import pytimekr
import datetime
import pymongo
if __name__ == "__main__":
    @app.route('/base_monitor/', methods=['POST'])
    def base_monitor():
        try:
            date = request.form['date']
            py_time = datetime.datetime.now()
            hour = py_time.hour
            min = py_time.minute
            if (hour == 15 and min >= 30) or hour > 15:
                hour = 15
                min = 30
            # hour = 15
            # min = 35

            total_time = (int)((hour * 60 + min - 9 * 60 - 5) / 5)
            if total_time <= 0:
                total_time = 78
            else:
                total_time += 1
            monitoring3_var = monitoring3(date)
            print("test1")
            monitoring3_var.preprocessProgram()
            time.sleep(2)
            monitoring3_var.preprocessForeign()
            monitoring3_var.preprocessPresent()
            print("test2")
            final_data = monitoring3_var.final_data
            final_data2 = monitoring3_var.final_data2
            final_data3 = monitoring3_var.final_data3
            # total_time = 75
            common_min_timeline_var2 = common_min_shortTime(5).timeline[:total_time]
        except Exception:
            return redirect(url_for('index'))
        return render_template('base_monitor.html', key=final_data.keys(), time_line=common_min_timeline_var2,values=final_data, values2=final_data2, values3=final_data3, length=total_time)
