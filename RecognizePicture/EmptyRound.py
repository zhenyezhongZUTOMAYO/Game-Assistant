import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import Recognize
import pyautogui
import cv2
import time
import threading
import pynput
import ctypes

import winsound
from AvoidStick import handle_stuck



class EmptyRound:

    def __init__(self):
        self.signal = []  # 什么都没识别到就是1
        self.lock = []

    def test(self):
        back = [self.signal[0], self.signal[1], self.signal[2], self.signal[3]]
        while True:
            if back[0] != self.signal[0]:
                # GanTan
                winsound.Beep(1000, 500)
                print(f"Gantan{self.signal}")
            if back[1] != self.signal[1]:
                # level
                winsound.Beep(400,500)
                print(f"门{self.signal}")
                pass
            if back[2] != self.signal[2]:
                # yd
                winsound.Beep(1000, 500)
                print(f"圆点{self.signal}")
            if back[3] != self.signal[3]:
                print(f"无{self.signal}")
            back = [self.signal[0], self.signal[1], self.signal[2], self.signal[3]]

    def testLock(self):
        back = self.lock
        while True:
            if self.lock[1] > back[1]:
                print(f"被上锁{self.lock}")
                winsound.Beep(1000, 500)
            elif self.lock[1] < back[1]:
                print(f"解锁一次{self.lock}")
                winsound.Beep(400, 500)
            back = self.lock

    def LookRound(self):
        # thread_test = threading.Thread(target=self.test)
        # thread_test.start()
        while True:
            if self.signal[0] & self.signal[1] & self.signal[2] & self.signal[3]:
                time.sleep(12)
                self.lock[0] += 1
                print(f"空房间环视一周：防卡上锁{self.lock}")
                round = 1
                while self.signal[0] & self.signal[1] & self.signal[2] & self.signal[3]:
                    if self.lock[1] > 0:
                        while self.lock[1] > 0:
                            time.sleep(1)
                            print("emt锁住!")
                        break
                    print(f"self.signal:{self.signal}")
                    ctypes.windll.user32.mouse_event(0x0001, 10, 0)
                    time.sleep(0.1)
                    round += 1
                    if round % 600 == 0:
                        handle_stuck()
                        if round >=1200:
                            keyboard = pynput.keyboard.Controller()
                            keyboard.press(pynput.keyboard.Key.space)
                            time.sleep(0.5)
                            keyboard.release(pynput.keyboard.Key.space)
                self.lock[0] -= 1
                print(f"空房间环视一周，防卡解锁{self.lock[0]}")
