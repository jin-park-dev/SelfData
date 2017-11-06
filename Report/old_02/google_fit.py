import Report.util_daily_report as util



tbl_name = 'google_fit'
date_name = 'Date'
start_date = '2017-01-01'
end_date = '2017-05-01' #23/07/2017
y_axis = 'Step count'

df = util.df_with_query(tbl_name, date_name, start_date, end_date)
util.plot_monthly(df[date_name], df[y_axis], tbl_name)

