import pandas as pd
import os
import sqlite3
import numpy as np
import Cleaning.cutil as cutil
from Report.util_report_config import *


# todo: important! some files contain "~" with same date. For now I deleted manually but later I automate this task. When i get new data I will run into this and error will be thrown.
# todo: found the bug. Only data is inconsistent. I started from 2011 previous which avoids all the bugs


def clean_pomodoro_excel():

    # ===== Config ========

    excel_pomodoro_path = r'D:\OneDrive\0 My Files\1 Documents\2 MS Office\1 Excel\2017\2 Pomodoro'


    # ===== Excel collection of multiple excel files ========


    excel_files = []
    excel_pomodoro_total_daily = pd.DataFrame(columns =['Date', 'pomo_total'])

    # =for dev purpose only=
    # excel_single_file_last = r'D:\OneDrive\0 My Files\1 Documents\2 MS Office\1 Excel\2017\2 Pomodoro\08-23.xlsx'
    # excel_single_file_first = r'D:\OneDrive\0 My Files\1 Documents\2 MS Office\1 Excel\2017\2 Pomodoro\04-11.xlsx'

    # ===== Reading CSV + Weight collection Cleaning ========
    # for file in [excel_single_file_last]:
    for file in os.listdir(excel_pomodoro_path):

        # for file in dev_smaller_files:
        try:
            print('file reading: {} \n'.format(file))
            xl = pd.ExcelFile(excel_pomodoro_path+ "\\" + file)
            #xl = pd.ExcelFile(file) #dev purpose only of reading single file.
            df_day = xl.parse("Sheet1", names=['time', 'subject', 'subject_non'], parse_cols= "B,C,D")
            df_day = df_day.dropna(axis=0, how='any', subset=['time'])
            df_day = df_day[df_day['time'] != 'Time']
            df_day = df_day.reset_index(drop=True)

            # Here for now I simplify to get total pomo per day, instead of having detailed day look
            df_day_temp = df_day.dropna(axis=0, how='any', subset=['subject'])
                #for now adding file names in simplified way
            day_sum = {'Date': [file],
                       'pomo_total': [len(df_day_temp)] }
            df_day_sum = pd.DataFrame(day_sum, columns=['Date', 'pomo_total'])
            excel_pomodoro_total_daily = excel_pomodoro_total_daily.append(df_day_sum)
            # print('\n\n')

        except IndexError:
            print("index error on file: {}".format(file))

    print("all files read")


    # For now assume it's only 2017 date. But later use folder to smartly decide. Probably in different stage of file.
    excel_pomodoro_total_daily['pomo_total'] = excel_pomodoro_total_daily['pomo_total'].astype(int)
    excel_pomodoro_total_daily['Date'] = excel_pomodoro_total_daily['Date'].str.replace('.xlsx', '')
    excel_pomodoro_total_daily['Date'] = "2017-" + excel_pomodoro_total_daily['Date']
    excel_pomodoro_total_daily['Date'] = pd.to_datetime(excel_pomodoro_total_daily['Date'], format="%Y-%m-%d")

    # print(excel_pomodoro_total_daily)
    # print(excel_pomodoro_total_daily.dtypes)



    # Dropping all the dates already in database

    tbl_name = daily_config['pomo_excel_daily']['tbl_name']

    excel_pomodoro_total_daily = cutil.get_only_new_data_df(excel_pomodoro_total_daily, tbl_name)




    # ===== Excel pomo saving to sqlite =====

    #TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

    conn = sqlite3.connect('selfdata_01.db')
    excel_pomodoro_total_daily.to_sql('pomo_excel_daily', conn, if_exists='append')


    conn.close()






