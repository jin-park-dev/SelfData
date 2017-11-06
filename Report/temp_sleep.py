import Report.util_daily_report as util

date_name = 'Date'

"""
# start_date = '2014-08-02'
# end_date = '2017-08-23'

start_date = '2017-01-01'
end_date = '2017-08-23'

tbl_name = 'sleep'
y_axis = 'total_hours'

df = util.df_with_query(tbl_name, date_name, start_date, end_date)
util.plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)
"""

#
# start_date = '2017-04-11'
# end_date = '2017-08-24'
#
# tbl_name = 'pomo_excel_daily'
# y_axis = 'pomo_total'
#
# df = util.df_with_query(tbl_name, date_name, start_date, end_date)
# util.plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)
#
#



start_date = '2016-09-01'
end_date = '2017-08-24'

tbl_name = 'pomo_kanban_daily'
y_axis = 'Total Pomo'

df = util.df_with_query(tbl_name, date_name, start_date, end_date)
util.plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)