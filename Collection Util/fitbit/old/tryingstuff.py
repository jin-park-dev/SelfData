# Code below makes python DPI aware
import pyautogui
import time
from ctypes import windll

# dpiFix = windll.user32
# dpiFix.SetProcessDPIAware()


#==============================

time.sleep(0.5)
# pyautogui.moveTo(568, 301, duration=0.25)
# pyautogui.click(button='left')
#
# pyautogui.moveTo(567, 341, duration=0.25)


# print(pyautogui.locateOnScreen('calendar.png'))
# print(pyautogui.locateOnScreen('calendar_end.png'))

# pyautogui.moveTo(568, 301, duration=0.25)

#
# pyautogui.dragRel(0, 500, duration=0.2, button='right')
# pyautogui.dragRel(0, -500, duration=0.1, button='right')


# pyautogui.hotkey('ctrl', 'r')

# cal_loc = pyautogui.locateAllOnScreen('s_cal.png')
# print(list(cal_loc))
cal_loc = pyautogui.locateOnScreen('cal_31_02.png')
print(print(cal_loc))

if cal_loc:
    print('True')

if not cal_loc:
    print('False')



# cal_outputs = [(863, 432, 34, 37),(866, 438, 30, 28), (866, 506, 30, 28)]
# for point in cal_outputs:
#     pyautogui.moveTo(point[0], point[1], duration=1)
#     time.sleep(0.5)

# pyautogui.moveTo(1003, 852)