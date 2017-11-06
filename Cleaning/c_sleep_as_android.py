import pandas as pd
import os
import sqlite3
import numpy as np
import datetime
import Cleaning.cutil as cutil
from Report.util_report_config import *


def clean_sleep_as_android():
    # ===== Config ========

    # data_root =

    path_sleep = r'D:\OneDrive\0 My Files\1 Documents\4 Raw Data\2 My Data\201x TO 2017-07-24\sleep-export.csv'


    # ===== Sleep as Android collection Cleaning ========
    cols = ['Id', 'Tz', 'From', 'To', 'Hours', 'Rating', 'Comment', 'Cycles', 'DeepSleep']

    sleep = pd.read_csv(path_sleep, usecols=cols)

    # === Fixing rows ===

    # Dropping duplicate label columns
    sleep = sleep[sleep['Id'] != "Id"]

    # Dropping Extra space columns
    sleep = sleep.dropna(subset=['Id'])

    # === Fixing columns (Dtypes) ===

    cols_dtype = {'Id': 'np.int64', 'Hours': float, 'Rating': np.float64, 'Cycles': int, 'DeepSleep': np.float64}


    sleep['Id'] = sleep['Id'].astype(np.int64)
    sleep['Hours'] = sleep['Hours'].astype(float)
    sleep['Rating'] = sleep['Rating'].astype(np.float64)
    sleep['Cycles'] = sleep['Cycles'].astype(int)
    sleep['DeepSleep'] = sleep['DeepSleep'].astype(np.float64)
    sleep['From'] = pd.to_datetime(sleep['From'], format='%d. %m. %Y %H:%M')
    sleep['To'] = pd.to_datetime(sleep['To'], format='%d. %m. %Y %H:%M')


    # print(sleep['From'])

    #Date 22. 08. 2017 16:52


    # Filtering, dropping columns has made index off.
    sleep = sleep.reindex(index=sleep.index[::-1])
    sleep = sleep.reset_index()
    sleep = sleep.drop('index', axis=1)

    # print(sleep.head())
    # print(sleep.tail())
    # print(sleep.dtypes)

    # [Rating, cycles, Deepsleep] do later
    # changing to dictionary style
    """
    for index, row in sleep.iterrows():
        # print('from')
        # print(sleep['From'].iloc[index])
        # print('to')
        # print(sleep['To'].iloc[index])
    
        # print(row.dtypes)
        # print(row)
        # print(index)
    
        # print(sleep.iloc[index]['From'])
        # print(type(sleep.iloc[index]['From']))
        # print(sleep['From'].iloc[index])
        # print(type(sleep['From'].iloc[index]))
    
    
        from_time = sleep['From'].iloc[index]
        # print(from_time.dt.date)
        # to_time_all = sleep['To'].iloc[index]
    
        # to_time_ = datetime.datetime(hour=to_time_all.hour, second=to_time_all.second)
    
        # if it's over 9pm
        if from_time.hour >= 9+12:
            from_time = from_time + pd.Timedelta(days=1)
            sleep_sum.loc[sleep_sum.index.max() + 1] = from_time.date() # shit how do i simply just add new data???
            # print(from_time.date())
    
            # start_date = start_date + datetime.timedelta(days
    
        # if sleep['From']
    """

    sleep_sum_dict = {}

    # init dict so I can look up and add values
    for index, row in sleep.iterrows():

        from_time = sleep['From'].iloc[index]
        # print(from_time.dt.date)
        # to_time_all = sleep['To'].iloc[index]
        # to_time_ = datetime.datetime(hour=to_time_all.hour, second=to_time_all.second)
        # if it's over 9pm
        if from_time.hour >= 9+12:
            from_time = from_time + pd.Timedelta(days=1)
            date = from_time.date()
            # print(date)
            # print('\n\n')
            sleep_sum_dict[date] = 0 # shit how do i simply just add new data???
        else:
            date = from_time.date()
            sleep_sum_dict[date] = 0

    for index, row in sleep.iterrows():

        from_time = sleep['From'].iloc[index]
        # print(from_time.dt.date)
        # to_time_all = sleep['To'].iloc[index]
        # to_time_ = datetime.datetime(hour=to_time_all.hour, second=to_time_all.second)
        # if it's over 9pm
        if from_time.hour >= 9+12:
            from_time = from_time + pd.Timedelta(days=1)
            date = from_time.date()
            sleep_sum_dict[date] += sleep.iloc[index]['Hours'] # shit how do i simply just add new data???
        else:
            date = from_time.date()
            sleep_sum_dict[date] += sleep.iloc[index]['Hours']

    # print(sleep_sum_dict)




    # print(sleep_sum_dict)





    # Fixing sleep hour to be 2 decimal place.
    # Making index ascending order from earliest date.
    # print(sleep_sum_dict)


    # print(list(sleep_sum_dict.items()))

    sleep_sum = pd.DataFrame(list(sleep_sum_dict.items()), columns=['Date', 'total_hours'])

    sleep_sum['total_hours'] = sleep_sum['total_hours'].round(2)
    sleep_sum['Date'] = pd.to_datetime(sleep_sum['Date'], format="%Y-%m-%d")
    sleep_sum = sleep_sum.sort_values('Date', axis=0)
    sleep_sum = sleep_sum.reset_index(drop=True)

    # print(sleep_sum['Date'].tail())


    # print(sleep_sum.dtypes)
    # print(sleep_sum)


    """
    print(sleep.head())
    print('==')
    print(sleep.tail())
    print(sleep.dtypes)
    """

    # TODO: Only works for sleep_sum not sleep. (Sleep sum shows total sleep per day)
    # Dropping all the dates already in database
    tbl_name = daily_config['sleep']['tbl_name']

    sleep_sum = cutil.get_only_new_data_df(sleep_sum, tbl_name)



    # ===== Sleep saving to sqlite =====

    #TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

    conn = sqlite3.connect('selfdata_01.db')
    # sleep.to_sql('sleep_all', conn)#, if_exists='append'
    sleep_sum.to_sql('sleep', conn, if_exists='append')
    conn.close()