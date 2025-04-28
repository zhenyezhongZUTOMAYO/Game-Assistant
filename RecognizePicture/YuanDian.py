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
        self.lock=[]
        self.one=False
        self.lockOne=False
        self.levelOne=False

    def RecognizeYuanDian(self):

        stop=0
        self.rec.pb()
        while True:

                print("开始识别    原点")
                next = [2, 3, 9, 15, 18]

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
                    self.rec.real=False
                    print(f"识别第{i}张图片")
                    try:
                        # 在屏幕上查找图片
                        if self.rec.end:
                            self.rec.va()
                            if self.one and not self.levelOne:
                                self.lock[2] -= 1
                                print(f"圆点:门解锁{self.lock[2]}")
                                self.levelOne=True
                            if self.one and not self.lockOne:
                                self.lock[0] -= 1
                                print(f"圆点:防卡解锁{self.lock}")
                                self.lockOne = True
                            print("退出")
                            return False
                        location = pyautogui.locateOnScreen(image_path_1, confidence=0.8)
                        if location is not None:
                            # 获取图片的中心坐标
                            self.rec.x, self.rec.y = pyautogui.center(location)
                            stop=0
                            self.signal[2]=0
                            self.rec.real=True
                            self.rec.va()
                            print("识别成功va()准备开始操作")
                            print(f"{i}:  第{i}张图片找到图片，坐标位于: ({self.rec.x}, {self.rec.y})")
                            self.rec.pb()
                        else:
                            pass
                            # print("未找到图片")
                    except Exception as e:
                        stop+=1
                        print(f"第{i}张图片未识别到")
                        if stop>6:
                            self.rec.real=False
                            self.rec.va()
                            print("va()准备开始操作")

                            # print("原点未识别到")
                            self.rec.end = True


                            return False
                        # print(f"发生错误: {e}")
                #----识别失败

                    # print("识别成功")
                    # print("识别失败")

    def trackingYuanDian(self,lock):
        self.one = False
        self.lockOne = False
        self.levelOne=False
        self.rec.end=False
        # print("******************************进入圆点\n")
        self.rec = Recognize.Recognize()
        thread_a = threading.Thread(target=self.RecognizeYuanDian)
        thread_a.start()
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        stick=0
        move=False
        avoid=False
        while True:
            #添加锁机制,如果一个函数运行时不希望其他程序识别时启用锁
            self.rec.pa()
            print("开始操作")
            print(f"a:{self.rec.sa}")
            print(f"b:{self.rec.sb}")
            # print("******************************圆点开始操作\n")
            # print("进入操作")
            if not thread_a.is_alive() or not self.rec.real:
                self.signal[2] = 1
                if self.one and not self.levelOne:
                    self.lock[2] -= 1
                    print(f"圆点:门解锁{self.lock[2]}")
                    self.levelOne = True
                if self.one and not self.lockOne:
                    self.lock[0] -= 1
                    print(f"圆点:防卡解锁{self.lock}")
                    self.lockOne = True
                print("检测到识别进程退出,退出")
                self.rec.vb()
                return False
            if self.lock[3]>0:
                while self.lock[3]>0:
                    print("圆点被锁住")
                    time.sleep(1)
                self.rec.end=True
                return False

            if not self.one:
                self.lock[2] += 1
                self.lock[0] += 1
                print(f"圆点:防卡上锁{self.lock[0]},门上锁{self.lock[2]}")
                self.one=True
            # print("正在操作")
                self.signal[2]=0
            if (abs(self.rec.x-center_x)>convert_coordinates(900,0,(3840,2160),rec.resolutionRatio)[0] or abs(self.rec.y-center_y)>convert_coordinates(0,580,(3840,2160),rec.resolutionRatio)[1] )and not avoid:
                stick+=1
                print(f"圆点不在中心,进行调整,第{stick}次调整")
                if stick>2:
                    # ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.rec.x - center_x) // 2)), ctypes.c_int(int((self.rec.y - center_y) // 2)))
                    avoid=True
                    stick=0
                move=False
            else:
                print("调整完成,开始行动")
                stick=0
                move=True
                avoid=True
                if not self.lockOne:
                    print("self.lockOne为 False")
                if self.one:
                    print("self.one为true")
                if self.one and not self.lockOne:
                    self.lock[0]-=1
                    print(f"圆点:防卡解锁{self.lock[0]}")
                    print(self.lock)
                    self.lockOne=True
            ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int((self.rec.x - center_x)//2), 0)
            print(f"x轴偏移{int((self.rec.x - center_x)//2)}")
            print(f"a:{self.rec.sa}")
            print(f"b:{self.rec.sb}")

            if  move:
                print("往前走进行操作")
                self.rec.keyboard.press('w')
                time.sleep(1)
                self.rec.keyboard.release('w')
            print("操作完成,准备识别")
            self.rec.vb()
            print(f"a:{self.rec.sa}")
            print(f"b:{self.rec.sb}")
if __name__=="__main__":
    yd=YuanDian()
    lock=[1,1]
    yd.trackingYuanDian(lock)
