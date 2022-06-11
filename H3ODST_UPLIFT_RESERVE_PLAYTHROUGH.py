from selgui import *
from lib2to3.pgen2 import driver
import time
import pyautogui
import pydirectinput

def play_mission():
    try:
        selgui.find(r'InCampaign/H3ODST/uplift_reserve/restart.png',.9)
        print("found restart button, going to restart current mission, assuming this is within the current challenge loop...")
        selgui.click(r'InCampaign/H3ODST/uplift_reserve/restart.png',.9)
        time.sleep(.25)
        selgui.click(r'InCampaign/H3ODST/uplift_reserve/yes.png',.9)
        time.sleep(2)
    except:
        print("no restart button found, continuing with mission...")
    print("starting Uplift Reserve automation mission now.")
    time.sleep(2)
    pydirectinput.keyDown('space')
    time.sleep(.25)
    pydirectinput.keyUp('space')
    print("skipped campaign cutscene")
    while True:
        try:
            selgui.find(r'InCampaign/H3ODST/uplift_reserve/start_confirm.png',.7)
            print("confirmed mission has started.")
            break
        except:
            pass
    print("beginning to move in script...")
    pydirectinput.mouseDown(button='left')
    pydirectinput.mouseUp(button='left')
    time.sleep(1)
    pydirectinput.keyDown('w')
    time.sleep(6)
    pydirectinput.keyUp('w')
    time.sleep(.25)
    pydirectinput.keyDown('w')
    pydirectinput.keyDown('d')
    time.sleep(25)
    pydirectinput.keyUp('w')
    pydirectinput.keyUp('d')

    time.sleep(1)
    pydirectinput.press('esc')