import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import date2num
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator, WeekdayLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import seaborn

file_loc = r'D:\OneDrive\0 My Files\0 System\3 Workspace\PycharmProjects\1 Personal Host Git\1 SelfData\Cleaning\selfdata_01.db'

conn = sqlite3.connect(file_loc)
c = conn.cursor()

# ====================

query = '''
SELECT * FROM weather_daily
LIMIT 60
''' #LIMIT 10
#ORDER BY DateOnly DESC


weather = pd.read_sql(query, con=conn)


# Currently latest plot_monthly. 07-Aug-20176
def plot_monthly(series_dates, series_record):

    series_dates = pd.to_datetime(series_dates, format="%Y-%m-%d %H:%M:%S")
    dates_list = []
    for i in series_dates:
        dates_list.append(i)

    date1 = dates_list[0]
    date2 = dates_list[len(dates_list)-1]

    years = YearLocator()   # every year
    months = MonthLocator(interval=1)  # every month
    days = DayLocator()
    loc = WeekdayLocator(byweekday=MO)
    dateFmt = DateFormatter('%d-%m-%Y %a')


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates_list, series_record)
    # plt.gcf().autofmt_xdate()

    # format the ticks
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(dateFmt)
    ax.xaxis.set_minor_locator(days)
    ax.autoscale_view()


    # def price(x):
    #     return '$%1.2f' % x
    # ax.fmt_xdata = DateFormatter('%Y-%m-%d')
    # ax.fmt_ydata = price
    # ax.grid(True)

    fig.autofmt_xdate()

    plt.show()

plot_monthly(weather['DateOnly'], weather['Temp_mean'])