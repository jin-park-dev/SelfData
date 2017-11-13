import pandas as pd
import os
import sqlite3
import numpy as np
import Cleaning.cutil as cutil
from Report.util_report_config import *
from Cleaning.util_config import root_dir



# todo: important! some files contain "~" with same date. For now I deleted manually but later I automate this task. When i get new data I will run into this and error will be thrown.
# todo: found the bug. Only data is inconsistent. I started from 2011 previous which avoids all the bugs


def clean_weather():

    # ===== Config ========

    # data_root =

    weather_path = r'D:\OneDrive\0 My Files\1 Documents\4 Raw Data\2 My Data\201x TO 2017-07-24\daily-text'


    # my_data_master=


    # ===== Weight collection of multiple csvs ========


    weather_files = []
    weather = pd.DataFrame()


    names = ['Time', 'Temp', 'Humid', 'DewPt', 'Press', 'WindSp', 'WindDr', 'Sun', 'Rain', 'Start', 'MxWSpd']

    drop_row_range = [i for i in range(8)]

    # For dev purpose, doing whole thing with smaller set of files.
    dev_smaller_files = os.listdir(weather_path)
    dev_smaller_files = dev_smaller_files[-50:-1]

    # ===== Reading CSV + Weight collection Cleaning ========
    for file in os.listdir(weather_path):
    # for file in dev_smaller_files:
        try:
            print('file reading: {} \n'.format(file))
            weather_monthly = pd.read_csv(weather_path+ "\\" + file, sep='\t', names=names)
            weather_monthly = weather_monthly.drop(weather_monthly.index[drop_row_range])
            # date is in file name itself so this needs to be added here.

            weather_monthly['DateOnly'] = file
            # print(weather_monthly['DateOnly'].head())
            weather_monthly['DateOnly'] = pd.to_datetime(weather_monthly['DateOnly'], format="%Y_%m_%d")
            # print(weather_monthly['DateOnly'].head())

            # TODO: Bug somewhere in data conversion. something to do with certain file or way it's processing.
            weather_monthly['Date'] = file + " " + weather_monthly['Time']
            # print(weather_monthly['Date'].head())
            weather_monthly['Date'] = pd.to_datetime(weather_monthly['Date'], format="%Y_%m_%d %H:%M")
            # print(weather_monthly['Date'].head())

            # print(weather_monthly['Temp'])
            # print(weather_monthly)

            weather_monthly['Temp'] = weather_monthly['Temp'].astype(np.float64)

            weather = weather.append(weather_monthly)

            print('\n\n')

        except IndexError:
            print("index error on file: {}".format(file))
            print("Might have no data for this date")

    print("all files read")

    # === Fixing columns (Dtypes) ===
    weather = weather.drop('Time', axis=1)

    # doing it in loop to catch bug
    # try:
    #     weather['Date'] = pd.to_datetime(weather['Date'], format="%Y_%m_%d %H:%M")
    # except:
    #     print("Error in date conversion")
    # try:
    #     weather['DateOnly'] = pd.to_datetime(weather['DateOnly'], format="%Y_%m_%d")
    # except:
    #     print("Error in DAteOnly conversion")

    # weather['Temp'] = weather['Temp'].astype(np.float64)
    weather['Humid'] = weather['Humid'].astype(np.int64)
    weather['DewPt'] = weather['DewPt'].astype(np.float64)

    weather['Press'] = weather['Press'].astype(np.int64)
    weather['WindSp'] = weather['WindSp'].astype(np.float64)

    weather['Sun'] = weather['Sun'].astype(np.float64)
    weather['Rain'] = weather['Rain'].astype(np.float64)
    weather['MxWSpd'] = weather['MxWSpd'].astype(np.int64)

    # == Column ordering with date first ==

    columns_order = ['DateOnly', 'Date', 'Temp', 'Humid', 'DewPt', 'Press', 'WindSp', 'WindDr', 'Sun', 'Rain', 'Start', 'MxWSpd']

    weather = weather[columns_order]

    # Reversing index for future
    weather = weather.sort_values('Date', axis=0)
    # weight = weight.reindex(index=weight.index[::-1])
    weather = weather.reset_index()
    weather = weather.drop('index', axis=1)


    #=========================
    # ====== Creating daily Database
    #=========================

    weather_hourly = weather.copy()
    # print(weather_hourly.head(10))
    weather_hourly = weather_hourly.groupby('DateOnly')
    # print(weather_hourly.head(10))


    weather_daily = weather_hourly.agg({'Temp': ['mean', 'min', 'max'], 'Humid': 'mean', 'Sun': 'max', 'Rain': 'max'})

    # print(weather_daily.head(2))

    # weather_daily = weather_daily.rename(columns={

    # weather_daily.columns = weather_daily.columns.droplevel(0)

    # Making 2 leveled columns into 1 again, but adding level 2 first. (e.g temp_max from just max)
    weather_daily.columns = ["_".join(x) for x in weather_daily.columns.ravel()]
    weather_daily = weather_daily.rename(columns={'Sun_max': 'Sun_total', 'Rain_max': 'Rain_total'})
    weather_daily = weather_daily.round(1)
    weather_daily = weather_daily.reset_index()
    # print(weather_daily.columns)

    # Naming to Date
    weather_daily['Date'] = weather_daily['DateOnly']
    weather_daily = weather_daily.drop('DateOnly', axis=1)

    col_reorder = ['Date', 'Temp_mean', 'Temp_min', 'Temp_max', 'Humid_mean', 'Sun_total',
                   'Rain_total']
    weather_daily = weather_daily[col_reorder]

    # print(weather_daily.columns)
    # print(weather_daily.head(22))




    # print("=======")
    # # print(weather_hourly.shape)
    # print("=======")
    # print(weather_hourly.head())
    # print("=======")
    # print(weather_hourly.tail())
    # print("=======")
    # print(weather_hourly.dtypes)




    # Dropping all the dates already in database
    tbl_name = daily_config['weather_daily']['tbl_name']

    weather_daily = cutil.get_only_new_data_df(weather_daily, tbl_name)



    # ===== weight saving to sqlite =====

    #TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

    conn = sqlite3.connect('selfdata_01.db')
    # weather.to_sql('weather_hourly', conn) #, if_exists='append'

    weather_daily.to_sql('weather_daily', conn, if_exists='append')

    conn.close()

