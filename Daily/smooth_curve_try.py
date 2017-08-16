import Daily.util_daily_report as util

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import date2num
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator, WeekdayLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import seaborn as sns
from sklearn.linear_model import LinearRegression



tbl_name = 'weight'
date_name = 'Date'
start_date = '2017-01-01'
end_date = '2017-04-01'
y_axis = 'Weight'


"""
def plot_monthly(series_dates, series_record, tbl_name):

    series_dates = pd.to_datetime(series_dates, format="%Y-%m-%d %H:%M:%S")
    dates_list = []
    for i in series_dates:
        dates_list.append(i)

    # date1 = dates_list[0]
    # date2 = dates_list[len(dates_list)-1]

    years = YearLocator()   # every year
    months = MonthLocator(interval=1)  # every month
    days = DayLocator()
    loc = WeekdayLocator(byweekday=MO)
    dateFmt = DateFormatter('%d-%m-%Y %a')


    # Best fit line

    df['days_since'] = (series_dates - pd.to_datetime(dates_list[0]) ).astype('timedelta64[D]')

    lr = LinearRegression()
    # print(len(series_dates))
    # print(len(df['days_since']))
    # print(len(series_record))

    lr.fit(df[['days_since', ]], series_record)
    predict = lr.predict(df[['days_since', ]])





    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates_list, series_record)
    ax.scatter(dates_list, series_record)

    ax.plot(dates_list, predict)

# sns.lmplot(dates_list, series_record, data=series_record, fit_reg=True)
    # plt.gcf().autofmt_xdate()

    # format the ticks
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(dateFmt)
    ax.xaxis.set_minor_locator(days)
    ax.autoscale_view()

    # name axis
    ax.set_xlabel(series_dates.name)
    ax.set_ylabel(series_record.name)
    ax.set_title(tbl_name) #Temp



    # def price(x):
    #     return '$%1.2f' % x
    # ax.fmt_xdata = DateFormatter('%Y-%m-%d')
    # ax.fmt_ydata = price
    # ax.grid(True)

    fig.autofmt_xdate()

    plt.show()
"""







# df = util.df_with_query(tbl_name, date_name, start_date, end_date)
# plot_monthly(df[date_name], df[y_axis], tbl_name)




