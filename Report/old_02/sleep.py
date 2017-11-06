import Report.util_daily_report as util


tbl_name = 'sleep'
date_name = 'To'
start_date = '2017-01-01'
end_date = '2017-04-01'
y_axis = 'Hours'

df = util.df_with_query(tbl_name, date_name, start_date, end_date)
util.plot_monthly(df[date_name], df[y_axis], tbl_name)

