# Code below makes python DPI aware
import pyautogui
import time
# from ctypes import windll
#
# dpiFix = windll.user32
# dpiFix.SetProcessDPIAware()

# USING CHROME.

# ================================================

# 24 Sep 2012 seems to be first log date
no_of_months = 5*12


for i in range(no_of_months):

    print('========== Run: {} ============'.format(i))

    #1. Refresh the page
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(2)

    #2. Get calendar locations
    cal_locs = list(pyautogui.locateAllOnScreen('cal_icon.png'))
    cal_start = (cal_locs[0][0], cal_locs[0][1])
    cal_end = (cal_locs[1][0], cal_locs[1][1])

    # print(cal_locs)
    # print(cal_start)
    # print(cal_end)

    #3. Click Start Date

    pyautogui.moveTo(cal_start, duration=0.25)
    pyautogui.click(button='left')
    back_cal_loc = pyautogui.locateOnScreen('cal_back.png')
    pyautogui.moveTo(back_cal_loc[0], back_cal_loc[1] , duration=0.25)

    #i+1 to start from first previous month (makes sense since you might not have all data this month)
    for j in range(i+1):
        pyautogui.click(button='left')

    start_date_loc = pyautogui.locateOnScreen('cal_01.png')
    pyautogui.moveTo(start_date_loc[0], start_date_loc[1], duration=0.25)
    pyautogui.click(button='left')

    #3. Click End Date

    pyautogui.moveTo(cal_end, duration=0.25)
    pyautogui.click(button='left')
    # back_cal_loc = pyautogui.locateOnScreen('cal_back.png')
    # pyautogui.moveTo(back_cal_loc[0], back_cal_loc[1] , duration=0.25)
    # for j in range(i+1):
    #     pyautogui.click(button='left')

    print('searching for end date')
    end_cal_list = ['cal_31.png', 'cal_30.png', 'cal_29.png', 'cal_28.png']
    cal_31 = pyautogui.locateOnScreen(end_cal_list[0])
    if cal_31:
        pyautogui.moveTo(cal_31[0], cal_31[1], duration=0.25)
        pyautogui.click(button='left')
    elif pyautogui.locateOnScreen(end_cal_list[1]):
        loc_cal_end = pyautogui.locateOnScreen(end_cal_list[1])
        pyautogui.moveTo(loc_cal_end[0], loc_cal_end[1], duration=0.25)
        pyautogui.click(button='left')
    elif pyautogui.locateOnScreen(end_cal_list[2]):
        loc_cal_end = pyautogui.locateOnScreen(end_cal_list[2])
        pyautogui.moveTo(loc_cal_end[0], loc_cal_end[1], duration=0.25)
        pyautogui.click(button='left')
    elif pyautogui.locateOnScreen(end_cal_list[3]):
        loc_cal_end = pyautogui.locateOnScreen(end_cal_list[3])
        pyautogui.moveTo(loc_cal_end[0], loc_cal_end[1], duration=0.25)
        pyautogui.click(button='left')
    else:
        print("Error: Couldn't find end date for i={}".format(i))

    #4. Press Download

    download_button_loc = pyautogui.locateOnScreen('download.png')
    pyautogui.click(button='left')

    time.sleep(4)



    # They must done something to image