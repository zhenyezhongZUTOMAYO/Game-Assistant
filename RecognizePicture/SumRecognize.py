import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import GanTanChat
import ChooseBuff
import YuanDian
import EnterNextLevel
import Recognize
import time
import threading
class SumRecognize:
    def __init__(self):
        #初始化类
        self.buff=ChooseBuff.BuffSelector()
        self.gantan=GanTanChat.GanTanChat()
        self.yd=YuanDian.YuanDian()
        self.level=EnterNextLevel.LevelSystem()
        self.gantan.BuffSelector=self.buff
        self.rec=Recognize.Recognize()
        #初始化锁
        self.lock=[]
        for i in range(0,2):
            self.lock.append(1)
        self.gantan.lock=self.lock
        self.buff.lock=self.lock


    def GanTan(self):
        while True:
            self.rec.ToRecognizeIfThen(self.rec.source_path+"Game-Assistant\\Source\\"+str(self.rec.resolutionRatio[0])+"GanTan.png",self.gantan.CommunicateToNpc)


    def YuanDian(self):
        while True:
            self.yd.trackingYuanDian(self.lock)

    def start(self):
        thread=[]
        # print("start")
        thread_gantan=threading.Thread(target=self.GanTan,args=[])
        thread.append(thread_gantan)
        thread_yd=threading.Thread(target=self.YuanDian,)
        thread.append(thread_yd)
        thread_level=threading.Thread(target=self.level.start,args=[self.lock,])
        thread.append(thread_level)
        self.buff.start()
        for thr in thread:
            thr.start()
        for thr in thread:
            thr.join()

    # def test(self):
    #     print(self.lock[0])
    #     self.gantan.test()
    #     print(self.lock[0])
