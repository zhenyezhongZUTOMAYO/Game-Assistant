import pyautogui
import cv2
import time
import os

class Recognize:

    def __init__(self):
        self.x=-1
        self.y=-1

    def ToRecognizeIsHave(self,image_path):
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if location is not None:
            return True
        else:
            return False

    def ToRecognizeWhere(self,image_path):
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if location is not None:
            self.x,self.y = pyautogui.center(location)
            return True
        else:
            return False

    def ToRecognizeConWhere(self,image_path):
        while True:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location is not None:
                self.x, self.y = pyautogui.center(location)
            else:
                return False

    def ToRecognizeIfThen(self,image_path,Fuction):
        while True:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location is not None:
                Fuction()
            else:
                time.sleep(1)

rec=Recognize()

