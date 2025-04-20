import threading

import pyautogui
import pynput
import time
import sys
import os
import Recognize
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class Fight:

    def __init__(self):
        self.mouse=pynput.mouse.Controller()
        self.keyborad=pynput.keyboard.Controller()
        self.rec=Recognize.Recognize()
        self.end=False
        self.lock=[]

    def A(self):
        while not self.end:
            self.mouse.press(pynput.mouse.Button.left)
            time.sleep(0.2)
            self.mouse.release(pynput.mouse.Button.left)
            time.sleep(0.2)
            self.mouse.press(pynput.mouse.Button.left)
            time.sleep(0.2)
            self.mouse.release(pynput.mouse.Button.left)
            time.sleep(0.2)
            self.mouse.press(pynput.mouse.Button.left)
            time.sleep(0.2)
            self.mouse.release(pynput.mouse.Button.left)
            time.sleep(0.2)
            self.mouse.press(pynput.mouse.Button.left)
            time.sleep(0.2)
            self.mouse.release(pynput.mouse.Button.left)
            time.sleep(0.2)
            self.mouse.press(pynput.mouse.Button.left)
            time.sleep(0.2)
            self.mouse.release(pynput.mouse.Button.left)
            if self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                    self.rec.resolutionRatio[0]) + "FullState.png",0.6):
                print("ZA")
                self.mouse.press(pynput.mouse.Button.left)
                time.sleep(8)
                self.mouse.release(pynput.mouse.Button.left)



    # def ZA(self):
    #     while not self.end:


    def MS(self):
        while not self.end:
            # print("MS")
            self.mouse.press(pynput.mouse.Button.right)
            time.sleep(0.5)
            self.mouse.release(pynput.mouse.Button.right)
            time.sleep(3)

    def isE(self):
        def convert_coordinates(x, y, original_res, target_res):
            """
            将坐标从原分辨率转换到目标分辨率
            :param x: 原坐标x
            :param y: 原坐标y
            :param original_res: 原分辨率 (width, height)
            :param target_res: 目标分辨率 (width, height)
            :return: 转换后的坐标 (new_x, new_y)
            """

            original_width, original_height = original_res
            target_width, target_height = target_res

            # 计算缩放比例
            scale_x = target_width / original_width
            scale_y = target_height / original_height

            # 转换坐标
            new_x = int(x * scale_x)
            new_y = int(y * scale_y)

            return new_x, new_y

        x, y = convert_coordinates(3342, 1900, (3840, 2160), self.rec.resolutionRatio)
        pixel =pixel_color = pyautogui.pixel(x, y)
        if pixel ==(255,255,255):
            return False
        else :
            return True

    def E(self):
        while not self.end:
            if self.isE():
                print("E")
                self.keyborad.press('e')
                time.sleep(0.5)
                self.keyborad.release('e')

    def Q(self):
        while not self.end:
            if self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                        self.rec.resolutionRatio[0]) + "Q.png"):
                self.keyborad.press('q')
                time.sleep(0.5)
                self.keyborad.release('q')
                stop=0
                now=time.time()
                while stop<25:
                    stop+=1
                    self.end=False
                    print(f"self.end=False{stop}")
                    time.sleep(0.2)
                print(f"总计用时{time.time()-now}")

    def R(self):
        if self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                self.rec.resolutionRatio[0]) + "R.png"):
            self.keyborad.press('r')
            time.sleep(0.5)
            self.keyborad.release('r')

    def FightEnd(self):
        while True:
            if not self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                        self.rec.resolutionRatio[0]) + "FightEnd.png"):
                self.end=True
                time.sleep(6)
                if not self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                        self.rec.resolutionRatio[0]) + "FightEnd.png"):
                    break
        for i in range(0, 4):
            self.lock[i] -= 1

    def ZC(self):
        while not self.end:
            while not self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                        self.rec.resolutionRatio[0]) + "ZC.png"):
                self.keyborad.press(pynput.keyboard.Key.space)
                time.sleep(0.5)
                self.keyborad.release(pynput.keyboard.Key.space)
                if self.end:
                    break
            if self.end:
                break
            time.sleep(20)
            if self.end:
                break
            while not self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                        self.rec.resolutionRatio[0]) + "ZC.png"):
                self.keyborad.press(pynput.keyboard.Key.space)
                time.sleep(0.5)
                self.keyborad.release(pynput.keyboard.Key.space)
                if self.end:
                    break
            self.keyborad.press(pynput.keyboard.Key.space)
            time.sleep(0.5)
            self.keyborad.release(pynput.keyboard.Key.space)
            if self.end:
                break
            Time=0
            if self.isE():
                Time+=3
            if self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                    self.rec.resolutionRatio[0]) + "Q.png"):
                Time+=5
            if self.end:
                break
            time.sleep(Time)
            self.keyborad.press(pynput.keyboard.Key.space)
            time.sleep(0.5)
            self.keyborad.release(pynput.keyboard.Key.space)
            if self.end:
                break
            Time=0
            if self.isE():
                Time+=3
            if self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                    self.rec.resolutionRatio[0]) + "Q.png"):
                Time+=5
            if self.end:
                break
            time.sleep(Time)
            if self.end:
                break
            self.keyborad.press(pynput.keyboard.Key.space)
            time.sleep(0.5)
            self.keyborad.release(pynput.keyboard.Key.space)
            if self.end:
                break

    # def Space(self):
    #     #这是在主C是第一位的情况下
    #     while True:
    #         time.sleep(20)
    #         self.keyborad.press(pynput.keyboard.Key.space)
    #         time.sleep(0.5)
    #         self.keyborad.release(pynput.keyboard.Key.space)
    #         time.sleep()

    def Fight(self):
        thread=[]
        # thread_za=threading.Thread(target=self.ZA)
        # thread.append(thread_za)
        thread_e=threading.Thread(target=self.E)
        thread.append(thread_e)
        thread_q=threading.Thread(target=self.Q)
        thread.append(thread_q)
        thread_ms = threading.Thread(target=self.MS)
        thread.append(thread_ms)
        thread_end=threading.Thread(target=self.FightEnd)
        thread.append(thread_end)
        thread_a=threading.Thread(target=self.A)
        thread.append(thread_a)
        thread_zc=threading.Thread(target=self.ZC)
        thread.append(thread_zc)
        thread_r=threading.Thread(target=self.R)
        thread.append(thread_r)
        for i in range(0,4):
            self.lock[i]+=1
        for i in thread:
            i.start()
        for i in thread:
            i.join()





if __name__ =="__main__":
    fight=Fight()
    fight.Fight()
#     print("开始测试")
#     time.sleep(2)
#     fight =Fight()
#     print("A")
#     fight.A()
#     time.sleep(2)
#     print("ZA")
#     fight.ZA()
#     time.sleep(2)
#     print("E")
#     fight.E()
#     time.sleep(2)
#     print("Q")
#     fight.Q()
#     time.sleep(2)
#     print("MS")
#     fight.MS()
#     time.sleep(2)
#     print("R")
#     fight.R()
#     time.sleep(2)