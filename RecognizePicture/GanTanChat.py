import Recognize
import pynput
import pyautogui
import threading
import time
class GanTanChat:
    def __init__(self):
        self.rec=Recognize.Recognize()

    def method(self,location,rec:Recognize.Recognize):
        self.rec.end=True
        self.rec.keyboard.release('w')
        keyboard = pynput.keyboard.Controller()

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
        keyboard.press('f')
        time.sleep(0.5)
        keyboard.release('f')
        self.Speak()

        keyboard.press('s')
        time.sleep(2)
        keyboard.release('s')

    def Speak(self):
        """
        这是一个与人对话的函数如果2秒内未出现与人交流的白点那么退出识别
        :return: None
        """
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
                stop += 1
                if stop > 3:
                    rec.end = True
            rec.vb()

    def CommunicateToNpc(self,confidence=0.8):
        # thread_a=threading.Thread(target=rec.ToRecognizeConWhere,args=[rec.source_path+"GanTan.png",])
        thread_b = threading.Thread(target=self.rec.ToRecognizeIfThen, args=[
            self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "Inter.png", self.method,
            confidence])
        # thread_a.start()
        thread_b.start()
        self.rec.trakingImage(self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "GanTan.png",confidence)