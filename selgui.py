import pyautogui
import time
class selgui:
    def click(element,confidence_value):
        x, y = pyautogui.locateCenterOnScreen(element, confidence=confidence_value)
        pyautogui.moveTo(x, y)
        pyautogui.click()
    def find(element,confidence_value):
        x, y = pyautogui.locateCenterOnScreen(element,confidence=confidence_value)  