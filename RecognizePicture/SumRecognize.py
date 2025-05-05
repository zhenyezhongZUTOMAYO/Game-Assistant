import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pyautogui
import pynput.keyboard
import GanTanChat
import ChooseBuff
import YuanDian
import EnterNextLevel
import Recognize
import time
import threading
import AvoidStick
import EmptyRound
import Fight


class SumRecognize:
    def __init__(self):
        #初始化类
        self.buff=ChooseBuff.BuffSelector()
        self.gantan=GanTanChat.GanTanChat()
        self.yd=YuanDian.YuanDian()
        self.level=EnterNextLevel.LevelSystem()
        self.gantan.BuffSelector=self.buff
        self.rec=Recognize.Recognize()
        self.avoid=AvoidStick.AvoidStick()
        self.emt=EmptyRound.EmptyRound()
        self.ft=Fight.Fight()
        self.level.As = self.avoid
        self.signal = []
        for i in range(0, 4):
            self.signal.append(1)
        self.gantan.signal=self.signal
        self.level.signal=self.signal
        self.yd.signal=self.signal
        # self.gantan.test()
        # print(f"gantan.signal{self.signal[0]}")
        self.emt.signal=self.signal
        #初始化锁
        self.lock=[]
        for i in range(0,4):
            self.lock.append(0)
        self.gantan.lock=self.lock
        self.buff.lock=self.lock
        self.avoid.lock=self.lock
        self.emt.lock=self.lock
        self.level.lock=self.lock
        self.ft.lock=self.lock
        self.yd.lock=self.lock

    def Fight(self):
        while True:
            if self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                    self.rec.resolutionRatio[0]) + "Fight.png"):
                print("识别到战斗开始")
                self.ft.Qsignal = False
                self.ft.Fight()
            elif self.rec.ToRecognizeWhere(self.rec.source_path + "Game-Assistant\\Source\\" + str(
                self.rec.resolutionRatio[0]) + "Fight1.png"):
                print("识别到战斗开始")
                self.ft.Qsignal = False
                self.ft.Fight()
            elif self.rec.RecognizeColor((2245,92),(0,255,0)):
                print("识别到战斗开始")
                self.ft.Qsignal=True
                self.ft.Fight()

    def GanTan(self):
        while True:
            self.rec.ToRecognizeIfThen(self.rec.source_path+"Game-Assistant\\Source\\"+str(self.rec.resolutionRatio[0])+"GanTan.png",self.gantan.CommunicateToNpc)
            if self.rec.ToRecognizeWhere(self.rec.source_path+"Game-Assistant\\Source\\"+str(self.rec.resolutionRatio[0])+"GanTan1.png"):
                keyboard=pynput.keyboard.Controller()
                keyboard.press('f')
                time.sleep(0.5)
                keyboard.press('f')
                rec = Recognize.Recognize()
                stop = 0
                while True:
                    rec.real=False
                    if rec.ToRecognizeWhere(rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "TestSpeak1.png",0.8):
                        rec.real=True
                    if rec.real:
                        pyautogui.click(rec.x, rec.y)
                        stop = 0
                    else:
                        """
                        识别不到的停止机制如果连续4次识别不到那么终止
                        """
                        # print("识别不到stop+1")
                        stop += 1
                        print("检测是否正在执行Buff")
                        if stop > 6:
                            break
                    if rec.ToRecognizeWhere(
                            rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "Option.png"):
                        pyautogui.click(rec.x, rec.y)
                keyboard.press('s')
                time.sleep(1.7)
                keyboard.release('s')


    def YuanDian(self):
        cishu=0
        while True:
            cishu+=1
            print(f"圆点启动{cishu}次")
            self.yd.trackingYuanDian(self.lock)


    def start(self):
        thread=[]
        print("start")
        thread_gantan=threading.Thread(target=self.GanTan,args=[])
        thread.append(thread_gantan)
        thread_yd=threading.Thread(target=self.YuanDian,)
        thread.append(thread_yd)
        thread_level=threading.Thread(target=self.level.start,args=[self.lock,])
        thread.append(thread_level)
        thread_avoid=threading.Thread(target=self.avoid.Solve)
        thread.append(thread_avoid)
        thread_emt=threading.Thread(target=self.emt.LookRound)
        thread.append(thread_emt)
        thread_ft=threading.Thread(target=self.Fight)
        thread.append(thread_ft)
        self.buff.start()
        thread_test=threading.Thread(target=self.test)
        thread_test.start()
        for thr in thread:
            thr.start()
        # while True:
        #     print("*******gantan.lock*******")
        #     print(self.gantan.lock)
        #     print("*******buff.lock*******")
        #     print(self.buff.lock)
        #     print("*******avoid.lock*******")
        #     print(self.avoid.lock)
        #     print("*******emt.lock*******")
        #     print(self.emt.lock)
        #     print("*******level.lock*******")
        #     print(self.ft.lock)
        #     print("*******level.lock*******")
        #     print(self.ft.lock)
        #     time.sleep(5)
        for thr in thread:
            thr.join()

    def test(self):
        time.sleep(12)
        self.lock[2]-=1
