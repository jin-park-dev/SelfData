import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import date2num
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, DayLocator, WeekdayLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import seaborn as sns
from sklearn.linear_model import LinearRegression
import datetime
from dateutil import relativedelta
from Daily.util_report_config import daily_config


# Config related
file_loc = r'D:\OneDrive\0 My Files\0 System\3 Workspace\PycharmProjects\1 Personal Host Git\1 SelfData\Cleaning\selfdata_01.db'


# =====================

conn = sqlite3.connect(file_loc)
c = conn.cursor()

# ====================

def df_with_query(table, date_name, start_date, end_date):


    query = '''
    SELECT * FROM {}
    WHERE "{}" BETWEEN date("{}") AND date("{}")
    '''.format(table, date_name, start_date, end_date)

    # print(query)

    df = pd.read_sql(query, con=conn)
    return df

# Currently latest plot_monthly. 14-Aug-20176
# x, y, table name, style (e.g ggplot), save (png to hard drive)
def plot_monthly(series_dates, series_record, tbl_name, start_date, end_date, style='fivethirtyeight', save=False):

    series_dates = pd.to_datetime(series_dates, format="%Y-%m-%d %H:%M:%S")

    # date_list is require to create x-axis
    dates_list = []
    for i in series_dates:
        dates_list.append(i)

    # date1 = dates_list[0]
    # date2 = dates_list[len(dates_list)-1]

    # print(dates_list[0])

    years = YearLocator()   # every year
    months = MonthLocator(interval=1)  # every month
    days = DayLocator(bymonthday=range(1,31,7)) #, interval=5
    loc = WeekdayLocator(byweekday=MO)
    dateFmt_Maj = DateFormatter('%d-%m-%Y %a')
    dateFmt_Min = DateFormatter('%d')



    # Best fit line

    df_temp = pd.DataFrame()
    df_temp['days_since'] = (series_dates - pd.to_datetime(dates_list[0])).astype('timedelta64[D]')

    lr = LinearRegression()
    # print(len(series_dates))
    # print(len(df_temp['days_since']))
    # print(len(series_record))

    lr.fit(df_temp[['days_since', ]], series_record)
    predict = lr.predict(df_temp[['days_since', ]])



    # Styling needs to be at top.
    plt.style.use(style)

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Ubuntu'
    plt.rcParams['font.monospace'] = 'Ubuntu Mono'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 18
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 12




    # Main part

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates_list, series_record, c='#DCD6F7', alpha=0.3) #dashes=(1,10), dash_capstyle='round', dash_joinstyle='round'
    ax.scatter(dates_list, series_record, c='#4E4C67', s=20, alpha=0.8)

    ax.plot(dates_list, predict, c='#A6B1E1', solid_capstyle='round')

    #print(plt.style.available)

    # sns.lmplot(dates_list, series_record, data=series_record, fit_reg=True)
    # plt.gcf().autofmt_xdate()

    # format the ticks
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(dateFmt_Maj)
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_minor_formatter(dateFmt_Min)
    # ax.autoscale_view()

    # Intelligently plot y-axis range

    lim_list = set_min_max_record(tbl_name, series_record.name, start_date, end_date)
    print('lim_list'.format(lim_list))
    ax.set_ylim(lim_list)


    # name axis
    ax.set_xlabel(removeUnderLine(series_dates.name), color='#5c5f6d')
    ax.set_ylabel(removeUnderLine(series_record.name), color='#5c5f6d')
    ax.set_title(removeUnderLine(tbl_name), color='#5c5f6d') #'#B4869F'


    # def price(x):
    #     return '$%1.2f' % x
    # ax.fmt_xdata = DateFormatter('%Y-%m-%d')
    # ax.fmt_ydata = price
    # ax.grid(True)

    fig.autofmt_xdate()

    if save:
        # Format file name to save
        file_date_start = datetime.datetime.strftime(series_dates.iloc[0], '%Y-%m-%d')
        file_date_end = datetime.datetime.strftime(series_dates.iloc[len(series_dates)-1], '%Y-%m-%d')

        fil_name = '{}_{}_to_{}_a01.png'.format(tbl_name, file_date_start, file_date_end)
        print(fil_name)
        plt.savefig(fil_name)

    plt.show()

# Removes underline and Cap the every word.
def removeUnderLine(string):
    string_fixed = string.replace("_", " ")
    string_fixed = string_fixed.title()
    return string_fixed

# Used to find find range of y-axis
def min_max_record(tbl_name, col):

    query = '''
    SELECT {tbl_name}.{col} FROM {tbl_name}
    '''.format(col=col, tbl_name=tbl_name)
    # print(query)

    series = pd.read_sql(query, con=conn)
    series_max = series.max()
    series_min = series.min()
    return series_min, series_max

# Returns array to set for y_lim (or x_lim)
def set_min_max_record(tbl_name, col, start_date, end_date):

    if tbl_name in daily_config:
        print('table( {} ) found in config. Using config to set y_lim'.format(tbl_name))

        # offset value not used yet

        config = daily_config[tbl_name]

        y_lim_offset = config['y_lim_offset']
        tbl_name = tbl_name
        date_name = config['date_name']
        y_axis = config['y_axis']
        y_lim_offset_percentage = config['y_lim_offset_percentage']

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        start_date = start_date + relativedelta.relativedelta(months=-y_lim_offset)
        # print(start_date)
        # print(type(start_date))
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = end_date + relativedelta.relativedelta(months=+y_lim_offset)
        # print(end_date)
        # print(type(end_date))


        df = df_with_query(tbl_name, date_name, start_date, end_date)
        series = df[y_axis]
        series_max = series.max()
        series_min = series.min()
        lim_min = series_min
        lim_max = series_max
        percent = ((lim_min+lim_max)/2)*y_lim_offset_percentage
        print('offset percentage value: '.format(percent))
        return [lim_min-percent, lim_max+percent]
        # return [lim_min-1, lim_max+1]





# For looking at whole of df
    query = '''
    SELECT "{col}" FROM {tbl_name}
    '''.format(col=col, tbl_name=tbl_name)

    # print(query)

    series = pd.read_sql(query, con=conn)
    # print(type(series))
    # print(series)
    series_max = series.max()
    series_min = series.min()
    lim_min = series_min.iloc[0]
    lim_max = series_max.iloc[0]
    ten_percent = ((lim_min+lim_max)/2)*0.10

    # print('lim min: {}'.format(lim_min))
    # print('lim max: {}'.format(lim_max))

    return [lim_min-ten_percent, lim_max+ten_percent]


if __name__ == '__main__':

    """
    tbl_name = 'weather_daily'
    date_name = 'Date'
    start_date = '2017-03-01'
    end_date = '2017-04-01'
    y_axis = 'Temp_mean'


    df = df_with_query(tbl_name, date_name, start_date, end_date)
    plot_monthly(df[date_name], df[y_axis], tbl_name)


    #min_max_record(tbl_name='mood', col='mood')
    #min_max_record(tbl_name='weather_daily', col='Temp_mean')
    

    tbl_name = 'mood'
    date_name = 'Date'
    start_date = '2017-01-01'
    end_date = '2017-04-01'
    y_axis = 'mood'

    df = df_with_query(tbl_name, date_name, start_date, end_date)
    plot_monthly(df[date_name], df[y_axis], tbl_name, style='ggplot')

    """


    tbl_name = 'weight'
    date_name = 'Date'
    start_date = '2017-04-01'
    end_date = '2017-04-30'
    y_axis = 'Weight'

    df = df_with_query(tbl_name, date_name, start_date, end_date)
    plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)

