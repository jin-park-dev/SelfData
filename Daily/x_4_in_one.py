import Daily.util_daily_report as util

date_name = 'Date'

start_date = '2017-01-01'
end_date = '2017-01-31'

# start_date = '2017-02-01'
# end_date = '2017-02-28'

# start_date = '2017-03-01'
# end_date = '2017-03-31'
#
# start_date = '2017-04-01'
# end_date = '2017-04-30'


tbl_name = 'weather_daily'
y_axis = 'Temp_mean'

df = util.df_with_query(tbl_name, date_name, start_date, end_date)
util.plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)


tbl_name = 'google_fit'
y_axis = 'Step count'

df = util.df_with_query(tbl_name, date_name, start_date, end_date)
util.plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date, style='seaborn-darkgrid')


tbl_name = 'mood'
y_axis = 'mood'

df = util.df_with_query(tbl_name, date_name, start_date, end_date)
util.plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)


tbl_name = 'weight'
y_axis = 'Weight'

df = util.df_with_query(tbl_name, date_name, start_date, end_date)
util.plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)