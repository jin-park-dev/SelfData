import Report.util_daily_report as util
from Report.util_report_config import daily_config
from dateutil import relativedelta

# from calendar import monthrange



import datetime

# Main drawing function
# Look ups "daily_config" and draws all the tables in the config file.
def graph_report(start_date, end_date):
    for tbl_name, tbl_info in daily_config.items():
        date_name = 'Date'
        df = util.df_with_query(tbl_name, date_name, start_date, end_date)
        # print(df)

        if df.empty:
            error = "Table: {}, No record for {} - {}".format(tbl_name, start_date, end_date)
            print(error)
            continue
            return error

        y_axis = tbl_info['y_axis']
        util.plot_monthly(df[date_name], df[y_axis], tbl_name, start_date, end_date)

#==============================================================================================

# Report function other will customize on

# Takes month as number (jan = 1, and returns graph of that period
def graph_report_months(year, month, month_lenth=0):

    start_date, end_date = util.find_dates(year, month, month_lenth)
    graph_report(start_date, end_date)


# Below are report functions
def graph_report_this_year():
    today = datetime.datetime.now() + relativedelta.relativedelta(months=0)
    start_date, end_date = util.find_dates(today.year, 1, 11)
    graph_report(start_date, end_date)


# Making year_lenth behaviour same as month_length
def graph_report_year(year, year_lenth):
    year_lenth = year_lenth+1
    start_date, end_date = util.find_dates(year, 1, 11*year_lenth)
    graph_report(start_date, end_date)


# This uses original way. refactor later.
def graph_report_previous_month():

    today = datetime.datetime.now() + relativedelta.relativedelta(months=0)

    start_date = datetime.datetime(today.year, today.month, 1)
    start_date = start_date + relativedelta.relativedelta(months=-1)
    end_date = start_date + relativedelta.relativedelta(months=+1, days=-1)

    # Due to SQL returning string, other function to draw graph expects string formatted time.
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    graph_report(start_date, end_date)

# Below are just customized graph_report_months for easy reporting.
def graph_report_past_3_month(year, month):

    start_date, end_date = util.find_dates(year, month, -3)
    graph_report(start_date, end_date)


def graph_report_past_6_month(year, month):

    start_date, end_date = util.find_dates(year, month, -6)
    graph_report(start_date, end_date)


def graph_report_past_year(year, month):

    start_date, end_date = util.find_dates(year, month, -12)
    graph_report(start_date, end_date)


if __name__ == '__main__':
    # graph_report_months(2017, 3)
    # graph_report_past_3_month(2017, 11)
    # graph_report_past_6_month(2017, 5)

    # graph_report_this_year()
    # graph_report_year(2016, year_lenth=0)
    # graph_report_year(2014, year_lenth=2)
    graph_report("2017-08-01", "2017-10-05")
