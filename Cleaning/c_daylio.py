import pandas as pd
import os
import sqlite3
import Cleaning.cutil as cutil
from Report.util_report_config import *


def clean_daylio():
    # ===== Config ========

    # data_root =

    path_daylio = r'D:\OneDrive\0 My Files\1 Documents\4 Raw Data\2 My Data\201x TO 2017-07-24\daylio_export.csv'


    # my_data_master=


    # ===== Daylio collection Cleaning ========

    daylio = pd.read_csv(path_daylio)


    # Fixing date

    daylio['year'] = daylio['year'].apply(str)
    daylio['date-str'] = daylio['date'] + ' ' + daylio['year'] + ' ' + daylio['time']
    daylio['date-datetime'] = pd.to_datetime(daylio['date-str'])

    # Dropping unrequired columns

    cols_drop_after_date = ['year', 'date', 'weekday', 'time', 'date-str']
    daylio = daylio.drop(cols_drop_after_date, axis=1)

    # Normalizing mood

    mood_map = {'awful': 0, 'fugly': 2.5, 'meh': 5, 'good': 7.5, 'rad': 10}
    daylio['mood'] = daylio['mood'].map(mood_map)


    # print(daylio.head())
    # print(daylio.dtypes)

    # Make date to each day
    daylio['Date'] = daylio['date-datetime'].dt.strftime('%Y-%m-%d')
    daylio = daylio.drop('date-datetime', axis=1)
    daylio = daylio[['Date', 'mood']]




    # Making average of the day from any hour of the day
    # WARNING: It drops other non-mean-able column automatically. But there's not much data on those so it's ok for now.
    daylio = daylio.groupby('Date')
    daylio = daylio.mean()
    daylio = daylio.reset_index()

    # Making date to date format again.
    #
    # print(daylio['Date'].head())
    # print(pd.api.types.is_string_dtype(daylio['Date']))
    daylio['Date'] = pd.to_datetime(daylio['Date'], format="%Y-%m-%d")
    # print(daylio.dtypes)

    """
    # Just checking there's no duplicate dates now.
    dates_counts = daylio['Date'].value_counts()
    dates_counts = dates_counts[dates_counts != 1]
    print("Below should be empty if there are no duplicate dates")
    print(dates_counts)
    """


    # print(daylio.head(55))

    # Dropping all the dates already in database
    tbl_name = daily_config['mood']['tbl_name']
    daylio = cutil.get_only_new_data_df(daylio, tbl_name)


    # Reversing index order
    # Not needed since index reset

    """
    daylio = daylio.reindex(index=daylio.index[::-1])
    daylio = daylio.reset_index()
    daylio = daylio.drop('index', axis=1)
    """



    # ===== Daylio saving to sqlite =====

    #TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

    conn = sqlite3.connect('selfdata_01.db')
    daylio.to_sql('mood', conn, if_exists='append') #
    conn.close()

if __name__ == '__main__':
    clean_daylio()