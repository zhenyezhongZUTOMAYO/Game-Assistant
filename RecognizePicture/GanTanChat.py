import Recognize
import pynput
import pyautogui
import threading
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
class GanTanChat:
    def __init__(self):
        self.rec=Recognize.Recognize()
        self.BuffSelector=None
        self.lock=[0,0]

    def method(self,rec,location):
        self.lock[0] = 0  #锁住圆点
        self.lock[1] = 0
        self.lock[2] = 0
        # print("锁住原点")
        rec.end=True
        rec.keyboard.release('w')
        rec.keyboard.release('w')
        keyboard = pynput.keyboard.Controller()
        if not rec.ToRecognizeWhere(rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "GanTan1.png"):
            keyboard.press('s')
            time.sleep(1)
            keyboard.release('s')
            keyboard.press('a')
            time.sleep(0.4)
            keyboard.release('a')
            rec.end = False  # 外部函数操控内部图象识别是否停止的变量
            rec.real = False  # 是否捕获到目标
            return
        # print("准备互动")
        # print("互动")
        keyboard.press('f')
        time.sleep(0.5)
        keyboard.release('f')
        self.Speak()
        # print(f"sa={self.rec.sa}\nsb={self.rec.sb}")
        self.lock[1]=0
        self.lock[2]=0
        keyboard.press('s')
        time.sleep(1.7)
        keyboard.release('s')
        self.lock[1]=1
        self.lock[0]=1  #释放原点
        self.lock[2]=1
        # print("释放原点")

    def Speak(self):
        """
        这是一个与人对话的函数如果2秒内未出现与人交流的白点那么退出识别
        :return: None
        """
        # print("Speak开始")
        rec = Recognize.Recognize()
        thread_a = threading.Thread(target=rec.ToRecognizeConWhere, args=[
            rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "TestSpeak1.png", ])
        thread_a.start()
        stop = 0
        while True:
            rec.pa()
            if not thread_a.is_alive():
                return
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
                if stop > 3:
                    rec.end = True
                    self.BuffSelector.pa()
                    self.BuffSelector.pa()
                    return
            rec.vb()
            if rec.ToRecognizeWhere(
                    rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "Option.png"):
                pyautogui.click(rec.x, rec.y)
        # print("Speak结束")

    def CommunicateToNpc(self,rec,location,confidence=0.8):
        print("开始识别     Gantan")
        # thread_a=threading.Thread(target=rec.ToRecognizeConWhere,args=[rec.source_path+"GanTan.png",])
        rec=Recognize.Recognize()
        thread_b = threading.Thread(target=rec.ToRecognizeIfThen, args=[
            self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "Inter.png", self.method,
            confidence])
        # thread_a.start()
        thread_b.start()

        rec.end=False
        #将识别门锁住
        self.lock[1]=0
        # print("trackingImage")
        # print(self.rec.end)
        # thread_avoidStick=threading.Thread(target=Solve,args=[rec,])
        # thread_avoidStick.start()
        rec.trakingImage(rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "GanTan.png",confidence,0.7)
        # print("trackingImageEnd")
        thread_b.join()
