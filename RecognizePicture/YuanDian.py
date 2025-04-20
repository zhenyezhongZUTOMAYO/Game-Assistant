import Recognize
import threading
import pyautogui
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import ctypes
from Recognize import rec

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

class YuanDian:
    def __init__(self):
        self.rec = Recognize.Recognize()
        self.location=None
        self.signal=[]
        self.one=False

    def RecognizeYuanDian(self):
        while True:
                self.rec.pb()
                print("开始识别    原点")
                next = [2, 3, 9, 15, 18]
                self.rec.real=False
                # image_path_1 = rec.source_path + "Game-Assistant\\Source\\" + str(
                #     rec.resolutionRatio[0]) + "YuanDian.png"
                #
                # try:
                #     # 在屏幕上查找图片
                #     location = pyautogui.locateOnScreen(image_path_1, confidence=0.8)
                #
                #     if location is not None:
                #         # 获取图片的中心坐标
                #         self.rec.x, self.rec.y = pyautogui.center(location)
                #         self.rec.real = True
                #         self.signal[2] = 0
                #         self.rec.va()
                #         print(f"找到图片，坐标位于: ({self.rec.x}, {self.rec.y})")
                #         break
                #     else:
                #         print("-原点未识别到")
                #         self.rec.va()
                #         if self.rec.end:
                #             return False
                #         # print("未找到图片")
                # except Exception as e:
                #     print("-原点未识别到")
                #     self.rec.va()
                #     if self.rec.end:
                #         return False


                for i in next:

                    image_path_1 = rec.source_path + "Game-Assistant\\Source\\" + str(
                        rec.resolutionRatio[0]) + f"Direction{i}.png"

                    try:
                        # 在屏幕上查找图片
                        if self.rec.end:
                            self.rec.va()
                            # print("退出")
                            return
                        location = pyautogui.locateOnScreen(image_path_1, confidence=0.8)

                        if location is not None:
                            # 获取图片的中心坐标
                            self.rec.x, self.rec.y = pyautogui.center(location)
                            self.rec.real=True
                            self.signal[2]=0
                            self.rec.va()
                            print(f"{i}:  第{i}张图片找到图片，坐标位于: ({self.rec.x}, {self.rec.y})")
                            break
                        else:
                            pass
                            # print("未找到图片")
                    except Exception as e:
                        pass
                        # print(f"发生错误: {e}")
                #----识别失败

                    # print("识别成功")
                if not self.rec.real:
                    print("-原点未识别到")
                    self.rec.va()
                    return
                    # print("识别失败")

    def trackingYuanDian(self,lock):
        self.rec.end=False
        # print("******************************进入圆点\n")
        thread_a = threading.Thread(target=self.RecognizeYuanDian)
        thread_a.start()
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        stick=0
        move=True
        avoid=False
        self.rec.sa = 0
        self.rec.sb = 1
        while True:
            #添加锁机制,如果一个函数运行时不希望其他程序识别时启用锁
            self.rec.pa()
            # print("******************************圆点开始操作\n")
            # print("进入操作")
            if not thread_a.is_alive():
                self.rec.vb()
                return False
            if lock[3]>0:
                while lock[3]>0:
                    print("圆点被锁住")
                    time.sleep(1)
                self.rec.end=True
                break
            if self.rec.real:
                if  not self.one:
                    lock[2] += 1
                    lock[0] += 1
                    self.one=True
                # print("正在操作")
                self.signal[2]=0
                stop=0
                if abs(self.rec.x-center_x)>convert_coordinates(900,0,(3840,2160),rec.resolutionRatio)[0] or avoid:
                    stick+=1
                    if stick>3:
                        # ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.rec.x - center_x) // 2)), ctypes.c_int(int((self.rec.y - center_y) // 2)))
                        avoid=True
                        stick=0
                    move=False

                else:
                    stick=0
                    move=True
                    lock[0]-=1
                ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.rec.x - center_x)//2)), 0)
            else:
                self.signal[2]=1
                print("原点未识别到")
                self.rec.end=True
                lock[2]-=1
                self.rec.vb()
                break
                # print("操作完成-误操作）
            if move:
                self.rec.keyboard.press('w')
                time.sleep(1)
                self.rec.keyboard.release('w')
            self.rec.vb()
if __name__=="__main__":
    yd=YuanDian()
    lock=[1,1]
    yd.trackingYuanDian(lock)
