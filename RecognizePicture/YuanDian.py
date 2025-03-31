import Recognize
import threading
import pyautogui
import time
import ctypes
class YuanDian:
    def __init__(self):
        self.rec=Recognize.Recognize()

    def trackingYuanDian(self):
        self.rec.end=False
        thread_a = threading.Thread(target=self.rec.ToRecognizeConWhere, args=[self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + f"Direction2.png", ])
        thread_a.start()
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        stop=0
        while True:
            self.rec.pa()
            # print("进入操作")
            if not thread_a.is_alive():
                self.rec.vb()
                return False
            if self.rec.real:
                # print("正在操作")
                ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.rec.x - center_x) / 2)), 0)
            else:
                stop+=1
                if stop>5:
                    self.rec.end=True
                    self.rec.vb()
                self.rec.vb()
                # print("操作完成-误操作")
                continue
            self.rec.keyboard.press('w')
            time.sleep(1)
            self.rec.keyboard.release('w')
            self.rec.vb()