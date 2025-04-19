import Recognize
import pyautogui
import cv2
import time
import os
import threading
import pynput
import ctypes
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class EmptyRound:

    def __init__(self):
        self.signal=[]#什么都没识别到就是1

    def LookRound(self):
        while True:

            if self.signal[0]&self.signal[1]&self.signal[2]&self.signal[3] :
                time.sleep(5)
                while self.signal[0]&self.signal[1]&self.signal[2]&self.signal[3]:
                    print(f"self.signal:{self.signal}")
                    ctypes.windll.user32.mouse_event(0x0001,10, 0)
                    time.sleep(0.1)


