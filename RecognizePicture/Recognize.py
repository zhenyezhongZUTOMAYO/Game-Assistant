import pyautogui
import cv2
import time
import os
import threading
import pynput
import ctypes
class Recognize:

    def __init__(self):
        self.x=-1
        self.y=-1
        self.sa=0 #获取到坐标的个数
        self.sb=1 #执行完操作的个数

    def pa(self):
        self.sa-=1
        while self.sa<0:
            time.sleep(0.2)

    def pb(self):
        self.sb-=1
        while self.sb<0:
            time.sleep(0.2)

    def va(self):
        self.sa+=1

    def vb(self):
        self.sb+=1

    def ToRecognizeIsHave(self,image_path):
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location is not None:
                return True
            else:
                return False
        except Exception:
            return False

    def ToRecognizeWhere(self,image_path):
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location is not None:
                self.x,self.y = pyautogui.center(location)
                return True
            else:
                return False
        except Exception :
            return False

    def ToRecognizeConWhere(self,image_path):
        while True:
            try:
                self.pb()
                location = pyautogui.locateOnScreen(image_path, confidence=0.8)
                if location is not None:
                    self.x, self.y = pyautogui.center(location)
                    self.va()
                else:
                    return False
            except Exception as e:
                self.va()
                return False

    def ToRecognizeIfThen(self,image_path,Fuction,Confidence=0.8):
        while True:
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=Confidence)
                if location is not None:
                    Fuction(location)
                    return
                else:
                    time.sleep(0.2)
            except Exception as e:
                time.sleep(0.2)

    def trakingImage(self,image_path):
        thread_a = threading.Thread(target=rec.ToRecognizeConWhere, args=[image_path, ])
        thread_a.start()
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        keyboard = pynput.keyboard.Controller()
        while True:
            rec.pa()
            if  not thread_a.is_alive():
                return False
            ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((rec.x-center_x)/2)) , ctypes.c_int(int((rec.y-center_y)/2)))
            keyboard.press('w')
            time.sleep(1)
            keyboard.release('w')
            rec.vb()

    # def click_image(self, image_path):
    #     try:
    #         location = pyautogui.locateOnScreen(image_path, confidence=0.7)
    #         if location is not None:
    #             x, y = pyautogui.center(location)  # 获取图像中心坐标
    #             pyautogui.click(x, y)  # 点击图像中心位置
    #     except Exception as e:
    #         return False

rec=Recognize()


