import pandas as pd
import os
import sqlite3
import numpy as np
import Cleaning.cutil as cutil
from Report.util_report_config import *
from datetime import datetime, timedelta

import sys

# todo: important! some files contain "~" with same date. For now I deleted manually but later I automate this task. When i get new data I will run into this and error will be thrown.
# todo: found the bug. Only data is inconsistent. I started from 2011 previous which avoids all the bugs


def clean_pomodoro_excel():

    # ===== Config ========

    excel_pomodoro_path = r'D:\OneDrive\0 My Files\1 Documents\2 MS Office\1 Excel\2017\2 Pomodoro'


    # ===== Excel collection of multiple excel files ========


    excel_files = []
    excel_pomodoro_total_daily = pd.DataFrame(columns =['Date', 'pomo_total'])
    excel_pomo = pd.DataFrame(columns =['Date', 'subject', 'subject_none'])
    excel_noo = pd.DataFrame(columns =['Date', 'nootropic'])

    # =for dev purpose only=
    # excel_single_file_last = r'11-13.xlsx'
    # excel_single_file_first = r'D:\OneDrive\0 My Files\1 Documents\2 MS Office\1 Excel\2017\2 Pomodoro\04-11.xlsx'
    # excel_single_file_first = r'04-11.xlsx'
    excel_single_file_custom = r'05-24.xlsx'

    # ===== Reading, processing Excel data for SQLDB ========
    # for file in [excel_single_file_custom]:
    for file in os.listdir(excel_pomodoro_path):

        # for file in dev_smaller_files:
        try:
            print('file reading: {} \n'.format(file))
            xl = pd.ExcelFile(excel_pomodoro_path+ "\\" + file)
            #xl = pd.ExcelFile(file) #dev purpose only of reading single file.
            #10-12.xlsx is start of nootropic.
            df_day = xl.parse("Sheet1", names=['time', 'subject', 'subject_none', 'nootropic'], parse_cols= "B,C,D,E")
            # For older when nootropic wasn't there.
            if df_day['nootropic'].iloc[0] != 'Nootropics':
                df_day = df_day.drop('nootropic', axis=1)
            # Gets rid of any empty data columns picked up on bottom of sheet, and excel-label at top.
            # If there's no time, there's no data.

            df_day = df_day.dropna(axis=0, how='any', subset=['time'])
            df_day = df_day[df_day['time'] != 'Time'] # Gets rid of excel-label but dropna is seems already doing it. But dropped index require this. Do i need drop index?
            df_day = df_day.reset_index(drop=True)


            # 1. excel_pomodoro_total_daily
            # Here for now I simplify to get total pomo per day, instead of having detailed day look
            df_day_temp = df_day.dropna(axis=0, how='any', subset=['subject'])
                #for now adding file names in simplified way
            day_sum = {'Date': [file],
                       'pomo_total': [len(df_day_temp)] }
            df_day_sum = pd.DataFrame(day_sum, columns=['Date', 'pomo_total'])
            excel_pomodoro_total_daily = excel_pomodoro_total_daily.append(df_day_sum)
            # print('\n\n')

            # 2. excel_raw, excel_noo

            # Add date column

            cur_month_day = file.replace('.xlsx', '')
            cur_year = os.path.basename(os.path.dirname(excel_pomodoro_path)) #This needs to be changed later
            cur_date = f'{cur_year}-{cur_month_day} '
            df_day['time'] = df_day['time'].astype(str)
            df_day['Date'] = cur_date + df_day['time']
            df_day['record_date'] = cur_date#2x + df_day['time']


            # Fixes cases where time goes past midnight so I have next date.
            # Added the recorded_date for today's pomodoro filters in SQL for future uses.
            try:
                df_day['Date'] = pd.to_datetime(df_day['Date'], format="%Y-%m-%d %H:%M:%S")
                #2xdf_day['record_date'] = pd.to_datetime(df_day['record_date'], format="%Y-%m-%d ")

            except ValueError:
                next_day = False
                for index, row in df_day.iterrows():
                    if next_day is False:
                        if row['time'] == '1900-01-01 00:00:00':
                            # print('ah... next day')
                            next_day = True
                            cur_date_datetime = datetime.strptime(cur_date, "%Y-%m-%d ")
                            tmr_date_datetime = cur_date_datetime + timedelta(days=1)
                            tmr_date_str = tmr_date_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            df_day.loc[index, 'Date'] = tmr_date_str
                            #2xdf_day.loc[index, 'record_date'] = cur_date_datetime
                            continue
                        row['Date'] = cur_date + row['time']
                        # row['record_date'] = cur_date
                    elif next_day is True:
                        # print('next_day stuff')
                        cur_date_datetime = datetime.strptime(cur_date, "%Y-%m-%d ")
                        tmr_date_datetime = cur_date_datetime + timedelta(days=1)
                        tmr_date_str = tmr_date_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        df_day.loc[index, 'Date'] = tmr_date_str
                        #2xdf_day.loc[index, 'record_date'] = cur_date_datetime

                df_day['Date'] = pd.to_datetime(df_day['Date'], format="%Y-%m-%d %H:%M:%S")
                #2xdf_day['record_date'] = pd.to_datetime(df_day['record_date'], format="%Y-%m-%d ")


        # prep for excel_pomo
            df_pomo = df_day[['Date', 'record_date', 'subject', 'subject_none']]
            # Add each day to bigger df
            excel_pomo = excel_pomo.append(df_pomo)

            if 'nootropic' in df_day.columns:
                df_noo = df_day[['Date', 'nootropic']]
                df_noo = df_noo.dropna(axis=0, how='any', subset=['nootropic']) # only keep time with data
                excel_noo = excel_noo.append(df_noo)

        except IndexError:
            print("index error on file: {}".format(file))

    print("\nall files read")


    # For now assume it's only 2017 date. But later use folder to smartly decide. Probably in different stage of file.
    excel_pomodoro_total_daily['pomo_total'] = excel_pomodoro_total_daily['pomo_total'].astype(int)
    excel_pomodoro_total_daily['Date'] = excel_pomodoro_total_daily['Date'].str.replace('.xlsx', '')
    excel_pomodoro_total_daily['Date'] = "2017-" + excel_pomodoro_total_daily['Date']
    excel_pomodoro_total_daily['Date'] = pd.to_datetime(excel_pomodoro_total_daily['Date'], format="%Y-%m-%d")

    # print(excel_pomodoro_total_daily)
    # print(excel_pomodoro_total_daily.dtypes)

    # print(excel_pomo.head())
    # print(excel_pomo.tail())
    #
    # print(excel_noo.head())
    # print(excel_noo.tail())



    # TODO: IMPORTANT!!! When appending ID is no longer going to be unique?????????????????? I think?????????????? Should I use SQLALCHEMY???
    # For now since it's getting it from start if I change below from append to remaking whole data it'll be ok.
    excel_pomo = excel_pomo.reset_index()
    excel_pomo = excel_pomo.drop('index', axis=1)
    print(excel_pomo)



    # Dropping all the dates already in database

    # TODO: DEL?
    # tbl_name_daily = daily_config['pomo_excel_daily']['tbl_name']
    # excel_pomodoro_total_daily = cutil.get_only_new_data_df(excel_pomodoro_total_daily, tbl_name_daily)

    tbl_name_pomo = daily_config['excel_pomodoro']['tbl_name']
    # Don't need for "if_exists='replace'"
    # excel_pomo = cutil.get_only_new_data_df(excel_pomo, tbl_name_pomo)

    tbl_name_noo = daily_config['excel_nootropic']['tbl_name']
    excel_noo = cutil.get_only_new_data_df(excel_noo, tbl_name_noo)




    # ===== Excel pomo saving to sqlite =====

    #TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

    conn = sqlite3.connect('selfdata_01.db')
    # TODO: DEL?
    excel_pomodoro_total_daily.to_sql('pomo_excel_daily', conn, if_exists='append')
    excel_pomo.to_sql(tbl_name_pomo, conn, if_exists='replace')
    excel_noo.to_sql(tbl_name_noo, conn, if_exists='append')


    conn.close()


if __name__ == '__main__':
    clean_pomodoro_excel()



