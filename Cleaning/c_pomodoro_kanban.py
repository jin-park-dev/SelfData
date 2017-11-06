import pandas as pd
import os
import sqlite3
import numpy as np
import Cleaning.cutil as cutil
from Report.util_report_config import *


def clean_pomodoro_kanban():

    # ===== Config ========

    # data_root =

    kanban_path = r'D:\OneDrive\0 My Files\1 Documents\4 Raw Data\2 My Data\201x TO 2017-07-24\Today board.csv'


    # my_data_master=


    # ===== Kanban collection Cleaning ========

    # cols = ['Name', 'Color', 'Time spent', 'Labels', 'Comments', 'Grouping date', 'Created timestamp']
    cols = ['Time spent', 'Grouping date']
    dtype = {'Time spent': np.float64}
    kanban = pd.read_csv(kanban_path, usecols=cols, dtype=dtype)

    # Fixing date
    kanban['Date'] = pd.to_datetime(kanban['Grouping date'], format='%Y-%m-%d')
    kanban.drop(['Grouping date'], inplace=True, axis=1)

    # Finding total pomo per day

    kanban = kanban.groupby('Date')
    kanban = kanban.sum()

    kanban = kanban.reset_index()

    # kanban['Time spent'] = kanban['Time spent'].round(2)
    # kanban['Time spent'] = kanban['Time spent'].astype(str)

    # print(kanban)

    # print(kanban['Time spent'].str.split('.').tolist())
    # kanban_temp = pd.DataFrame(kanban['Time spent'].str.split('.').tolist(), columns = ['Hour', 'Min'])

    """
    
    kanban = pd.concat([kanban, kanban_temp], axis=1)
    kanban['Hour'] = kanban['Hour'].astype(np.int)
    kanban['Min'] = kanban['Min'].astype(np.int)
    kanban['Min2'] = (kanban['Min'] * 60) % 60
    kanban['pomo_total'] = kanban['Hour']*60 + kanban['Min']
    """


    def dec_norm(time):
        hours = int(time)
        minutes = (time*60) % 60
        seconds = (time*3600) % 60
        # print("%d:%02d:%02d" % (hours, minutes, seconds))
        total_min = hours*60 + minutes
        return total_min


    #Covert decimal time to normal time
    kanban['Total Min'] = kanban['Time spent'].apply(dec_norm)

    kanban['pomo_total'] = kanban['Total Min'] / 26
    # Round to nearest
    kanban['pomo_total'] = kanban['pomo_total'].round(0)
    kanban = kanban.drop(['Time spent', 'Total Min'], axis=1)

    # print(kanban)


    # Dropping all the dates already in database

    tbl_name = daily_config['pomo_kanban_daily']['tbl_name']

    kanban = cutil.get_only_new_data_df(kanban, tbl_name)



    # ===== Kanban saving to sqlite =====

    #TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

    conn = sqlite3.connect('selfdata_01.db')
    kanban.to_sql('pomo_kanban_daily', conn, if_exists='append')
    conn.close()
