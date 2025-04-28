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
        self.lock=[]

    def LookRound(self):
        while True:
            if self.signal[0]&self.signal[1]&self.signal[2]&self.signal[3] :
                time.sleep(12)
                self.lock[0]+=1
                print(f"空房间环视一周：防卡上锁{self.lock}")
                while self.signal[0]&self.signal[1]&self.signal[2]&self.signal[3]:
                    if self.lock[1]>0:
                        while self.lock[1]>0:
                            time.sleep(1)
                        break
                    print(f"self.signal:{self.signal}")
                    ctypes.windll.user32.mouse_event(0x0001,10, 0)
                    time.sleep(0.1)
                self.lock[0]-=1
                print(f"空房间环视一周，防卡解锁{self.lock[0]}")

