import pyautogui
import pynput
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class Fight:

    def __init__(self):
        self.mouse=pynput.mouse.Controller()
        self.keyborad=pynput.keyboard.Controller()

    def A(self):
        pyautogui.click()

    def ZA(self):
        self.mouse.press(pynput.mouse.Button.left)
        time.sleep(3)
        self.mouse.release(pynput.mouse.Button.left)

    def MS(self):
        self.mouse.press(pynput.mouse.Button.right)
        time.sleep(0.5)
        self.mouse.release(pynput.mouse.Button.right)

    def E(self):
        self.keyborad.press('e')
        time.sleep(0.5)
        self.keyborad.release('e')

    def Q(self):
        self.keyborad.press('q')
        time.sleep(0.5)
        self.keyborad.release('q')

    def R(self):
        self.keyborad.press('r')
        time.sleep(0.5)
        self.keyborad.release('r')

    def Space(self):
        self.keyborad.press(pynput.keyboard.Key.space)
        time.sleep(0.5)
        self.keyborad.release(pynput.keyboard.Key.space)

if __name__ =="__main__":
    print("开始测试")
    time.sleep(2)
    fight =Fight()
    print("A")
    fight.A()
    time.sleep(2)
    print("ZA")
    fight.ZA()
    time.sleep(2)
    print("E")
    fight.E()
    time.sleep(2)
    print("Q")
    fight.Q()
    time.sleep(2)
    print("MS")
    fight.MS()
    time.sleep(2)
    print("R")
    fight.R()
    time.sleep(2)