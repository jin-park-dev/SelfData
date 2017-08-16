import pandas as pd
import os
import sqlite3
import numpy as np


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
        weather_monthly = pd.read_csv(weather_path+ "\\" + file, sep='\t', names=names)
        weather_monthly = weather_monthly.drop(weather_monthly.index[drop_row_range])
        # date is in file name itself so this needs to be added here.
        weather_monthly['DateOnly'] = file
        weather_monthly['Date'] = file + " " +weather_monthly['Time']
        weather = weather.append(weather_monthly)
    except IndexError:
        print("index error on file: {}".format(file))
        print("Might have no data for this date")

    
# === Fixing columns (Dtypes) ===
weather = weather.drop('Time', axis=1)

weather['Date'] = pd.to_datetime(weather['Date'], format="%Y_%m_%d %H:%M")
weather['DateOnly'] = pd.to_datetime(weather['DateOnly'], format="%Y_%m_%d")

weather['Temp'] = weather['Temp'].astype(np.float64)
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

print(weather_daily.columns)
print(weather_daily.head(22))




# print("=======")
# # print(weather_hourly.shape)
# print("=======")
# print(weather_hourly.head())
# print("=======")
# print(weather_hourly.tail())
# print("=======")
# print(weather_hourly.dtypes)








# ===== weight saving to sqlite =====

#TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

conn = sqlite3.connect('selfdata_01.db')
weather.to_sql('weather_hourly', conn) #, if_exists='append'

weather_daily.to_sql('weather_daily', conn) #, if_exists='append'

conn.close()

