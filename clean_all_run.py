from Cleaning.c_daylio import *
from Cleaning.c_google_fit_summary import *
from Cleaning.c_pomodoro_excel import *
from Cleaning.c_pomodoro_kanban import *
from Cleaning.c_sleep_as_android import *
from Cleaning.c_weather import *
from Cleaning.c_weight import *


if __name__ == '__main__':
    print('Cleaning all the data')
    clean_daylio()
    clean_google_fit_summary()
    clean_pomodoro_excel()
    clean_pomodoro_kanban()
    clean_sleep_as_android()
    clean_weather()
    clean_weight()
    print('All cleaning done')