import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import date2num
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator


file_loc = r'D:\OneDrive\0 My Files\0 System\3 Workspace\PycharmProjects\1 Personal Host Git\1 SelfData\Cleaning\selfdata_01.db'

conn = sqlite3.connect(file_loc)
c = conn.cursor()

# ====================

query = '''
SELECT * FROM mood
''' #LIMIT 10
#ORDER BY DateOnly DESC


mood = pd.read_sql(query, con=conn)

# weather['DateOnlyStr'] = datetime.datetime(weather['DateOnly']).strftime('%d/%m/%Y')

#Fuck no time. Just hacking so it shows something. I need to figure out right and elegant way to plot x for time.

# x = [i for i in range(len(weather['DateOnly']))]

# For some reason datetime object is converted to str. Maybe sqlalchemy would be better ?
# print(mood.dtypes)
# print(mood.head())






def plot_monthly(series_dates, series_record):

    series_dates = pd.to_datetime(series_dates, format="%Y-%m-%d %H:%M:%S")
    dates_list = []
    for i in series_dates:
        dates_list.append(i)

    date1 = dates_list[0]
    date2 = dates_list[len(dates_list)-1]

    years = YearLocator()   # every year
    months = MonthLocator()  # every month
    days = DayLocator()
    dateFmt = DateFormatter('%d-%m-%Y')


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates_list, series_record)
    # plt.gcf().autofmt_xdate()

    # format the ticks
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(dateFmt)
    # ax.xaxis.set_minor_locator(days)
    ax.autoscale_view()

    # def price(x):
    #     return '$%1.2f' % x
    # ax.fmt_xdata = DateFormatter('%Y-%m-%d')
    # ax.fmt_ydata = price
    # ax.grid(True)

    fig.autofmt_xdate()

    plt.show()

plot_monthly(mood['date-datetime'], mood['mood'])








"""


mood['DateOnly'] = mood['DateOnly'].str.replace(' 00:00:00', '')
mood['DateOnly'] = pd.to_datetime(mood['DateOnly'], format="%Y-%m-%d") # %H:%M:%S


# for i in weather['DateOnly']:
#     print(type(i))
#     print(i)


# x = date2num(weather['DateOnly'])
# print(x)

# plt.plot(x, weather['Temp_mean'])
# plt.show()



# Second way

# pd.DataFrame.plot
mood.plot(x='DateOnly', y='Temp_mean')

plt.xticks()


plt.show()

"""