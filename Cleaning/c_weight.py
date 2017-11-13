import pandas as pd
import os
import sqlite3
import numpy as np
import Cleaning.cutil as cutil
from Report.util_report_config import *
from Cleaning.util_config import root_dir



def clean_weight():

    # ===== Config ========

    fitbit_path = r'D:\OneDrive\0 My Files\1 Documents\4 Raw Data\2 My Data\201x TO 2017-07-24\weight'


    # ===== Weight collection of multiple csvs ========


    weight_files = []
    weight = pd.DataFrame()


    #fitbit_path+"\\"+"fitbit_export_20170725 (1).csv"
    names = ['Date', 'Weight', 'BMI', 'Fat']


    # Not parsing yet


    # ===== Reading CSV + Weight collection Cleaning ========
    for file in os.listdir(fitbit_path):
        weight_montly = pd.read_csv(fitbit_path+ "\\" + file, names=names, dtype={'Date': object}) #, parse_dates=['Date'], date_parser=date_parser
        weight_montly = weight_montly.drop(weight_montly.index[[0, 1]])

        try:
            weight_montly['Date'] = pd.to_datetime(weight_montly['Date'], format="%d-%m-%Y")
        except:
            print(file)
            print('Problem in parsing date %d-%m-%Y format. Trying to Parse with 2nd format.')
            try:
                weight_montly['Date'] = pd.to_datetime(weight_montly['Date'], format="%d/%m/%Y")

                print('parsed date in "%d/%m/%Y format instead')
            except:
                print('DATE ISSUE: error in parsing date %d-%m-%Y format.')

        weight = weight.append(weight_montly)

        ###


    # === Fixing columns (Dtypes) ===

    weight['Weight'] = weight['Weight'].astype(np.float64)
    weight['BMI'] = weight['BMI'].astype(np.float64)
    weight['Fat'] = weight['Fat'].astype(np.float64)


    # Reversing index for future
    weight = weight.sort_values('Date', axis=0)
    # weight = weight.reindex(index=weight.index[::-1])
    weight = weight.reset_index()
    weight = weight.drop('index', axis=1)


    # print("=======")
    # print(weight.shape)
    # print("=======")
    # print(weight.head(3))
    # print("=======")
    # print(weight.tail())
    # print("=======")
    # print(weight.dtypes)
    # print(weight['Date'].head(3))

    """
    # ==== Fill in with estimate missing dates =====
    
    print("=======")
    print("=======")
    
    # print(weight['Date'].iloc[0])
    # print(weight['Date'].iloc[len(weight)-1])
    
    # weight = weight.groupby('Date')
    # weight = weight['Date'].resample
    
    print(weight.head(10))
    start_date = weight['Date'].iloc[0]
    latest_date = weight['Date'].iloc[len(weight)-1]
    all_dates = pd.date_range(start_date, latest_date)
    
    weight = pd.DatetimeIndex(weight.index)
    weight = weight.reindex(all_dates, fill_value="NaN")
    
    
    print("=======")
    print(weight.shape)
    print(weight.head(10))
    
    print("=======")
    """



    # Dropping all the dates already in database
    tbl_name = daily_config['weight']['tbl_name']

    weight = cutil.get_only_new_data_df(weight, tbl_name)







    # ===== weight saving to sqlite =====

    #TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

    conn = sqlite3.connect('selfdata_01.db')
    weight.to_sql('weight', conn, if_exists='append')

    conn.close()




