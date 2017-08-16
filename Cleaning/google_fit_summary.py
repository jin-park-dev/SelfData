import pandas as pd
import os
import sqlite3
import numpy as np


# ===== Config ========

# data_root =

fit_agg_path = r'D:\OneDrive\0 My Files\1 Documents\4 Raw Data\2 My Data\201x TO 2017-07-24\Takeout\Fit\Daily Aggregations\Daily Summaries.csv'


# my_data_master=


# ===== Google fit agg collection Cleaning ========

cols = ['Date', 'Calories (kcal)', 'Step count', 'Cycling duration (ms)' , 'Inactive duration (ms)', 'Walking duration (ms)', 'Running duration (ms)']


g_fit = pd.read_csv(fit_agg_path, usecols=cols)

# Fixing date

g_fit['Date'] = pd.to_datetime(g_fit['Date'])



# Reversing index for future
g_fit = g_fit.reindex(index=g_fit.index[::-1])
g_fit = g_fit.reset_index()
g_fit = g_fit.drop('index', axis=1)


# === Filling empty values with 0 ===
g_fit = g_fit.fillna(value=0, axis='columns')

# print(g_fit.head())
# print(g_fit['Step count'].head())

# === Fixing columns (Dtypes) ===

dtype_map = {'Calories (kcal)': float, 'Step count': int, 'Inactive duration (ms)': int, 'Cycling duration (ms)': int, 'Walking duration (ms)': int, 'Running duration (ms)': int}

# g_fit['Calories (kcal)'] = g_fit['Calories (kcal)'].astype(float)
g_fit['Step count'] = g_fit['Step count'].astype(np.int64)
g_fit['Inactive duration (ms)'] = g_fit['Inactive duration (ms)'].astype(np.int64)
g_fit['Cycling duration (ms)'] = g_fit['Cycling duration (ms)'].astype(np.int64)
g_fit['Walking duration (ms)'] = g_fit['Walking duration (ms)'].astype(np.int64)
g_fit['Running duration (ms)'] = g_fit['Running duration (ms)'].astype(np.int64)

# print(g_fit.dtypes)
# print(g_fit.columns)

print(g_fit.head())

# ===== Daylio saving to sqlite =====

#TODO: need to look at how to manage data if it's already in database. Way it's working now i'll get duplicates

conn = sqlite3.connect('selfdata_01.db')
g_fit.to_sql('google_fit', conn) #, if_exists='append'
conn.close()