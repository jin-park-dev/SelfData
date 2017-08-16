import Daily.util_daily_report as util


tbl_name = 'weight'
date_name = 'Date'
start_date = '2017-03-01'
end_date = '2017-03-31'
y_axis = 'Weight'

df = util.df_with_query(tbl_name, date_name, start_date, end_date)
util.plot_monthly(df[date_name], df[y_axis], tbl_name)