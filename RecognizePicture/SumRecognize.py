import GanTanChat
import ChooseBuff
import YuanDian
import time
import Recognize
import threading
class SumRecognize:
    def __init__(self):
        self.buff=ChooseBuff.BuffSelector()
        self.gantan=GanTanChat.GanTanChat()
        self.yd=YuanDian.YuanDian()
        self.gantan.BuffSelector=self.buff
        self.rec=Recognize.Recognize()

    def GanTan(self):
        while True:
            self.rec.ToRecognizeIfThen(self.rec.source_path+"Game-Assistant\\Source\\"+str(self.rec.resolutionRatio[0])+"GanTan.png",self.gantan.CommunicateToNpc)

    def YuanDian(self):
        while True:
            self.rec.ToRecognizeIfThen(self.rec.source_path+"Game-Assistant\\Source\\"+str(self.rec.resolutionRatio[0])+"Direction2.png",self.yd.trackingYuanDian)
            time.sleep(5)

    def start(self):
        thread=[]
        print("start")
        thread_gantan=threading.Thread(target=self.GanTan,args=[])
        thread.append(thread_gantan)
        thread_yd=threading.Thread(target=self.YuanDian,args=[])
        thread.append(thread_yd)
        self.buff.start()
        for thr in thread:
            thr.start()
        for thr in thread:
            thr.join()


