import pandas as pd
import os
import sqlite3
import numpy as np

import datetime

# ===== Config ========

# data_root =

fitbit_path = r'D:\OneDrive\0 My Files\1 Documents\4 Raw Data\2 My Data\201x TO 2017-07-24\weight'


# my_data_master=


# ===== Weight collection of multiple csvs ========


weight_files = []
weight = pd.DataFrame()


#fitbit_path+"\\"+"fitbit_export_20170725 (1).csv"
names = ['Date', 'Weight', 'BMI', 'Fat']


# Not parsing yet
def date_parser(d):
    d = datetime.datetime.strptime(d, "%d/%m/%Y")
    return d



# ===== Reading CSV + Weight collection Cleaning ========
for file in os.listdir(fitbit_path):
    weight_montly = pd.read_csv(fitbit_path+ "\\" + file, names=names, dtype={'Date': str}) #, parse_dates=['Date'], date_parser=date_parser
    weight_montly = weight_montly.drop(weight_montly.index[[0, 1]])

    try:
        weight_montly['Date'] = pd.to_datetime(weight_montly['Date'], format="%d-%m-%Y")
    except:
        print('error in parsing date %d-%m-%Y format.')
        try:
            weight_montly['Date'] = pd.to_datetime(weight_montly['Date'], format="%d/%m/%Y")
            print('parsed date in "%d/%m/%Y format instead')
        except:
            print('DATE ISSUE: error in parsing date %d-%m-%Y format.')




    #weight['Date'] = pd.to_datetime(weight['Date']) #

    weight = weight.append(weight_montly)

    ###

    # Trying to fix date that's messed up.

    print("====="*30)
    print(file)
    print("====="*30)
    print(weight_montly['Date'].head(1))
    print(weight_montly['Date'].tail(1))
    print("====="*30)

    # print(weight_montly['Weight'].any())


    # print(weight_montly['Date'].head())
    # weight_date_check = weight_montly[weight_montly['Date'] == "01-05-2017"]
    # print(weight_date_check)


    #2017-06-02, 2017-10-05
    #10-05-2017  x05-10-2017

    if '05-10-2017' in weight_montly['Date'].unique():
        print('this is ok')
        print('2017-10-05 found at {}'.format(file))

    if '10-05-2017' in weight_montly['Date'].unique():
        print('error found')
        print('2017-10-05 found at {}'.format(file))

    ###


# print(weight_montly.head(32))
# print(weight_montly.iloc[0:1])
# print(weight_montly.index[0:2])


# if '10-05-2017' in weight_montly['Date'].unique():
#     print()
#     print('error date in weight_montly after conversion')


# === Fixing columns (Dtypes) ===

#Doing this above because of bug
# weight['Date'] = pd.to_datetime(weight['Date']) #, format="%d-%m-%Y"

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

# WIP
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










# ===== weight saving to sqlite =====

#TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

conn = sqlite3.connect('selfdata_01.db')
weight.to_sql('weight', conn) #, if_exists='append'

conn.close()




