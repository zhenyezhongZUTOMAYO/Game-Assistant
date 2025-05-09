import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import Recognize
import pynput
import pyautogui
import threading
import time

import ctypes

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class GanTanChat:
    def __init__(self):
        self.rec = Recognize.Recognize()
        self.BuffSelector = None
        self.lock = [0, 0]
        self.keyboard = pynput.keyboard.Controller()
        self.avoidNpc = 0  # 闪避Npc一定次数不必闪避
        self.signal = []
        self.one = False
        self.unlock = False
        self.recognize = False
        self.s = [1, ]  # 0unlock变量锁
        self.isMethod = False

    def p(self, n):
        self.s[n] -= 1
        while self.s[n] < 0:
            time.sleep(0.1)

    def v(self, n):
        self.s[n] += 1

    def setSignal(self):
        self.signal[0] = 0
        for i in range(0, 10):
            print(f"信号{self.signal}")
            time.sleep(1)
        if not self.recognize:
            self.signal[0] = 1

    def method(self, rec, location):
        self.signal[0] = 0
        # print(f"感叹:3防卡上锁{self.lock[0]}")
        # print("锁住原点")
        keyboard = pynput.keyboard.Controller()
        if not rec.ToRecognizeWhere(
                rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "GanTan1.png"):
            # if self.avoidNpc <= 2:
            #     keyboard.press('s')
            #     time.sleep(1)
            #     keyboard.release('s')
            #     keyboard.press('a')
            #     time.sleep(0.4)
            #     keyboard.release('a')
            #     self.avoidNpc += 1
            rec.end = True  # 外部函数操控内部图象识别是否停止的变量
            rec.real = False  # 是否捕获到目标
            self.recognize = False
            thread_signal = threading.Thread(target=self.setSignal)
            thread_signal.start()
            self.p(0)
            if self.one and not self.unlock:
                self.lock[2] -= 1
                print(f"G1门解锁{self.lock}")
                self.lock[3] -= 1
                # winsound.Beep(700, 1000)
                self.unlock = True
            self.v(0)
            keyboard.press('w')
            time.sleep(0.5)
            keyboard.release('w')
            print(f"感叹:1防卡解锁{self.lock[0]},圆点解锁{self.lock[3]}")
            return
        # print("准备互动")
        # print("互动")
        # 代表此次追踪Npc已结束
        self.lock[0] += 1
        self.avoidNpc = 0
        print("F!")
        for i in range(0, 3):
            keyboard.press('f')
            time.sleep(0.2)
            keyboard.release('f')
            time.sleep(0.2)
        self.Speak()
        # print(f"sa={self.rec.sa}\nsb={self.rec.sb}")
        # 以防万一再锁一次
        keyboard.press('s')
        time.sleep(1.7)
        keyboard.release('s')
        rec.end = True
        self.signal[0] = 1
        print("信号设置为1")
        self.lock[0] -= 1
        if self.one and not self.unlock:
            self.lock[2] -= 1
            print(f"G2门解锁{self.lock}")
            self.lock[3] -= 1
            # winsound.Beep(700, 200)
            self.unlock = True
        print(f"感叹:2防卡解锁{self.lock[0]},圆点解锁{self.lock[3]}")
        # print(f"释放圆点{self.lock[3]}")
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
                if stop > 6:
                    rec.end = True
                    self.BuffSelector.pa()
                    self.BuffSelector.pa()
                    return
            rec.vb()
            if rec.ToRecognizeWhere(
                    rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "Option.png"):
                pyautogui.click(rec.x, rec.y)
        # print("Speak结束")

    def CommunicateToNpc(self, rec, location, confidence=0.8):
        self.isMethod = False
        self.one = False
        self.unlock = False
        print("开始识别     Gantan")
        # thread_a=threading.Thread(target=rec.ToRecognizeConWhere,args=[rec.source_path+"GanTan.png",])
        rec = Recognize.Recognize()
        rec.signal = self.signal
        thread_b = threading.Thread(target=rec.ToRecognizeColorIfThen, args=[self.method])
        thread_b.daemon = True
        thread_b.start()
        # thread_b = threading.Thread(target=rec.ToRecognizeIfThen, args=[
        #     self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "Inter.png", self.method,
        #     confidence])
        # # thread_a.start()
        # thread_b.start()

        rec.end = False
        # 将识别门锁住

        # print("trackingImage")
        # print(self.rec.end)
        # thread_avoidStick=threading.Thread(target=Solve,args=[rec,])
        # thread_avoidStick.start()
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        stop = 0
        while True:
            if self.rec.ToRecognizeWhere(
                    rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "GanTan.png"):
                if not self.one:
                    self.lock[2] += 1
                    print(f"G3门上锁{self.lock}")
                    self.lock[3] += 1
                    # winsound.Beep(500, 500)
                    print(f"感叹:4原点上锁{self.lock[3]}")
                    self.one = True
                if rec.end:
                    break
                self.signal[0] = 0
                self.recognize = True
                ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.rec.x - center_x) // 2)), 0)
                self.keyboard.press('w')
                time.sleep(0.5)
                self.keyboard.release('w')
            elif self.rec.ToRecognizeWhere(
                    rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "GanTan1.png"):
                if rec.end:
                    break
                self.signal[0] = 0
                #有没有修改过信号量
                self.recognize = True
                if self.rec.y < (center_y / 2):
                    self.keyboard.press('s')
                    time.sleep(1)
                    self.keyboard.release('s')
                ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.rec.x - center_x) // 2)), 0)
                self.keyboard.press('w')
                time.sleep(0.5)
                self.keyboard.release('w')
            else:
                stop += 1
                if stop > 3:
                    if self.isMethod:
                        thread_b.join()
                        break
                    self.signal[0] = 1
                    rec.end = True
                    break
        self.p(0)
        if self.one and not self.unlock:
            self.lock[2] -= 1
            print(f"G4门解锁{self.lock}")
            self.lock[3] -= 1
            #winsound.Beep(700, 500)
            self.unlock = True
            print(f"感叹:0防卡解锁{self.lock[0]},圆点解锁{self.lock[3]}")
        self.v(0)
        thread_b.join()
        # print("trackingImageEnd")

    # 测试
    # def test(self):
    #     rec = Recognize.Recognize()
    #     rec.signal=self.signal
    #     thread_test=threading.Thread(target=rec.trakingImage,args=[rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "GanTan.png",0.8,0.7,0])
    #     thread_test.start()
    #     time.sleep(2)
    #     rec.end=True
    #     print(self.signal[0])
