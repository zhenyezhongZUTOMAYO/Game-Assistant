import Recognize
import threading
import pyautogui
import time
import ctypes
from Recognize import rec
class YuanDian:
    def __init__(self):
        self.rec = Recognize.Recognize()
        self.location=None

    def RecognizeYuanDian(self):
        while True:
                self.rec.pb()
                if self.rec.end:
                    self.rec.va()
                    # print("退出")
                    return
                print("开始识别    原点")
                next = [2, 3, 9, 15, 18]
                self.rec.real=False
                for i in next:
                    image_path_1 = rec.source_path + "Game-Assistant\\Source\\" + str(
                        rec.resolutionRatio[0]) + f"Direction{i}.png"

                    try:
                        # 在屏幕上查找图片
                        location = pyautogui.locateOnScreen(image_path_1, confidence=0.8)

                        if location is not None:
                            # 获取图片的中心坐标
                            self.rec.x, self.rec.y = pyautogui.center(location)
                            self.rec.real=True
                            self.rec.va()
                            print(f"{i}:  第{i}张图片找到图片，坐标位于: ({self.rec.x}, {self.rec.y})")
                        else:
                            print("未找到图片")
                    except Exception as e:
                        print(f"发生错误: {e}")
                #----识别失败

                    # print("识别成功")
                if not self.rec.real:
                    self.rec.va()
                    # print("识别失败")
                    if self.rec.end:
                        return False

    def trackingYuanDian(self,lock):
        self.rec.end=False
        thread_a = threading.Thread(target=self.RecognizeYuanDian)
        thread_a.start()
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        stop=0
        while True:
            #添加锁机制,如果一个函数运行时不希望其他程序识别时启用锁
            if lock[0]==0:
                self.rec.real=False
                while lock[0]==0:
                    print("原点被锁住!")
                    time.sleep(1)
            self.rec.pa()
            print("原点开始执行")
            # print("进入操作")
            if not thread_a.is_alive():
                self.rec.vb()
                return False
            if self.rec.real:
                print("正在操作")
                stop=0
                ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.rec.x - center_x) / 2)), 0)
            else:
                stop+=1
                if stop>3:
                    print("原点未识别到")
                    self.rec.end=True
                self.rec.vb()
                # print("操作完成-误操作")
                continue
            self.rec.keyboard.press('w')
            time.sleep(1)
            self.rec.keyboard.release('w')
            self.rec.vb()