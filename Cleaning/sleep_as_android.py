import pandas as pd
import os
import sqlite3
import numpy as np

np.int
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
sleep['From'] = pd.to_datetime(sleep['From'])
sleep['To'] = pd.to_datetime(sleep['To'])


# print(sleep.head())
# print(sleep.tail())
# print(sleep.dtypes)

# Filtering, dropping columns has made index off.
sleep = sleep.reindex(index=sleep.index[::-1])
sleep = sleep.reset_index()
sleep = sleep.drop('index', axis=1)



print(sleep.head())
print('==')
print(sleep.tail())
print(sleep.dtypes)


"""

# ===== Sleep saving to sqlite =====

#TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

conn = sqlite3.connect('selfdata_01.db')
sleep.to_sql('sleep', conn)#, if_exists='append'
conn.close()

"""
