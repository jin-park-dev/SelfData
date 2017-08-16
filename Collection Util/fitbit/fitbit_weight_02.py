# Code below makes python DPI aware
import pyautogui
import time
# from ctypes import windll
#
# dpiFix = windll.user32
# dpiFix.SetProcessDPIAware()

# USING CHROME.

# ================================================


def click_start_date():
    start_cal_start = (cal_start[0]+10, cal_start[1]+100)
    cal_box_x_offset = 137
    cal_box_y_offset = 136

    cal_box_00 = start_cal_start
    cal_box_10 = (start_cal_start[0]+cal_box_x_offset, start_cal_start[1])
    cal_box_11 = (start_cal_start[0]+cal_box_x_offset, start_cal_start[1]+cal_box_y_offset)
    cal_box_01 = (start_cal_start[0], start_cal_start[1]+cal_box_y_offset)

    pyautogui.moveTo(cal_box_00, duration=0.25)
    pyautogui.moveTo(cal_box_10, duration=0.25)
    pyautogui.moveTo(cal_box_11, duration=0.25)
    pyautogui.moveTo(cal_box_01, duration=0.25)

    target_pixel_color = (66,111,217)
    pyautogui.moveTo(cal_box_00, duration=0.25)

    for y_offset in range(0, cal_box_y_offset, 5):
        for x_offset in range(0, cal_box_x_offset, 10):
            pyautogui.moveTo(cal_box_00[0]+x_offset, cal_box_00[1]+y_offset)
            if pyautogui.pixelMatchesColor(cal_box_00[0]+x_offset, cal_box_00[1]+y_offset, (target_pixel_color)):
                print("Match found at")
                print(cal_box_00[0]+x_offset, cal_box_00[1]+y_offset)
                pyautogui.click(button='left')
                return


def click_end_date():
    end_cal_end = (cal_end[0]+10, cal_end[1]+100)
    cal_box_x_offset = 137
    cal_box_y_offset = 136

    cal_box_00 = end_cal_end
    cal_box_10 = (end_cal_end[0]+cal_box_x_offset, end_cal_end[1])
    cal_box_11 = (end_cal_end[0]+cal_box_x_offset, end_cal_end[1]+cal_box_y_offset)
    cal_box_01 = (end_cal_end[0], end_cal_end[1]+cal_box_y_offset)

    pyautogui.moveTo(cal_box_00, duration=0.25)
    pyautogui.moveTo(cal_box_10, duration=0.25)
    pyautogui.moveTo(cal_box_11, duration=0.25)
    pyautogui.moveTo(cal_box_01, duration=0.25)

    target_pixel_color = (66,111,217)
    pyautogui.moveTo(cal_box_00, duration=0.25)

    for y_offset in range(cal_box_y_offset, 0, -5):
        for x_offset in range(cal_box_x_offset, 0, -10):
            pyautogui.moveTo(cal_box_00[0]+x_offset, cal_box_00[1]+y_offset)
            if pyautogui.pixelMatchesColor(cal_box_00[0]+x_offset, cal_box_00[1]+y_offset, (target_pixel_color)):
                print("Match found at")
                print(cal_box_00[0]+x_offset, cal_box_00[1]+y_offset)
                pyautogui.click(button='left')
                return














# 24 Sep 2012 seems to be first log date
no_of_months = 5*12


for i in range(no_of_months):

    print('========== Run: {} ============'.format(i))

    #1. Refresh the page
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(5)

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

    pyautogui.moveTo(cal_start, duration=0.25)
    pyautogui.click(button='left')
    click_start_date()

    #3. Click End Date

    pyautogui.moveTo(cal_end, duration=0.25)
    pyautogui.click(button='left')
    click_end_date()

    #4. Press Download

    download_button_loc = pyautogui.locateOnScreen('download.png')
    pyautogui.moveTo(download_button_loc[0], download_button_loc[1] , duration=0.05)
    pyautogui.click(button='left')

    time.sleep(10)



    # They must done something to image