import pyautogui
import time


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


time.sleep(1)
pyautogui.hotkey('ctrl', 'r')

#2. Get calendar locations
cal_locs = list(pyautogui.locateAllOnScreen('cal_icon.png'))
cal_start = (cal_locs[0][0], cal_locs[0][1])
cal_end = (cal_locs[1][0], cal_locs[1][1])

#3. Click Start Date
pyautogui.moveTo(cal_start, duration=0.25)
pyautogui.click(button='left')

click_start_date()

#3. Click End Date
pyautogui.moveTo(cal_end, duration=0.25)
pyautogui.click(button='left')

click_end_date()