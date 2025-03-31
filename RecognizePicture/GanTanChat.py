import Recognize
import pynput
import pyautogui
import threading
import time
class GanTanChat:
    def __init__(self):
        self.rec=Recognize.Recognize()
        self.BuffSelector=None

    def method(self):
        self.rec.end=True
        self.rec.keyboard.release('w')
        keyboard = pynput.keyboard.Controller()
        rec=Recognize.Recognize()
        if not rec.ToRecognizeWhere(rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "GanTan1.png"):
            keyboard.press('s')
            time.sleep(0.5)
            keyboard.release('s')
            keyboard.press('a')
            time.sleep(0.5)
            keyboard.release('a')
            self.rec.end = False  # 外部函数操控内部图象识别是否停止的变量
            self.rec.real = False  # 是否捕获到目标
            self.CommunicateToNpc()
            return
        print("准备互动")
        if not rec.ToRecognizeWhere(rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "Inter.png"):
            print("回退互动")
            keyboard.press('s')
            time.sleep(0.5)
            keyboard.release('s')
        print("互动")
        keyboard.press('f')
        time.sleep(0.5)
        keyboard.release('f')
        self.Speak()
        # print(f"sa={self.rec.sa}\nsb={self.rec.sb}")

        keyboard.press('s')
        time.sleep(2)
        keyboard.release('s')


    def Speak(self):
        """
        这是一个与人对话的函数如果2秒内未出现与人交流的白点那么退出识别
        :return: None
        """
        print("Speak开始")
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
                print("识别不到stop+1")
                stop += 1
                print("检测是否正在执行Buff")
                loop=self.BuffSelector.loop
                if self.BuffSelector.buff == True or (stop > 3 and self.BuffSelector.loop-loop > 1):
                    rec.end = True
                    print(f"buff为{self.BuffSelector.buff}")
                    while self.BuffSelector.buff:
                        print("循环...")
                        time.sleep(1)
                    while self.BuffSelector.loop-loop>1:
                        time.sleep(0.2)
            rec.vb()
            if rec.ToRecognizeWhere(
                    rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "Option.png"):
                pyautogui.click(rec.x, rec.y)
        print("Speak结束")

    def CommunicateToNpc(self,confidence=0.8):
        # thread_a=threading.Thread(target=rec.ToRecognizeConWhere,args=[rec.source_path+"GanTan.png",])
        thread_b = threading.Thread(target=self.rec.ToRecognizeIfThen, args=[
            self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "Inter.png", self.method,
            confidence])
        # thread_a.start()
        thread_b.start()
        # print("trackingImage")
        self.rec.trakingImage(self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "GanTan.png",confidence)
        self.rec.end=False
        # print("trackingImageEnd")
