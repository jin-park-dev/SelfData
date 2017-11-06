import sqlite3
import datetime
import numpy as np

#TODO: "Date" table column name is hardset here. If I change "Date" column name I need to change by hand. Use config like other file later.

def get_latest_db_date(tbl_name):

    conn = sqlite3.connect('selfdata_01.db')
    cur = conn.cursor()
    query_latest_db_date = '''
      SELECT Date FROM {}
      ORDER BY Date DESC
      LIMIT 1
     '''.format(tbl_name)
    latest_db_date_return = cur.execute(query_latest_db_date)
    latest_db_date = latest_db_date_return.fetchone()[0]
    # print(latest_db_date)
    try:
        latest_db_date = datetime.datetime.strptime(latest_db_date, "%Y-%m-%d")
    except:
        latest_db_date = datetime.datetime.strptime(latest_db_date, "%Y-%m-%d %H:%M:%S")
    latest_db_date = np.datetime64(latest_db_date)
    # print(latest_db_date)
    conn.close()
    return latest_db_date


# TODO: Bit hacky way to get all the dates.
def get_only_new_data_df(df, tbl_name):

    try:
        latest_db_date = get_latest_db_date(tbl_name)
    except sqlite3.OperationalError:
        print("Issue: seems like database doesn't exist yet. We'll add for first time now.")
        latest_db_date = datetime.datetime.strptime("1990-07-22 00:00:00", "%Y-%m-%d %H:%M:%S")
    filter_tb = df['Date'] > latest_db_date
    df = df[filter_tb]

    print('new data to add for {}'.format(tbl_name))
    print(df.head())
    print(df.tail())
    print()

    return df