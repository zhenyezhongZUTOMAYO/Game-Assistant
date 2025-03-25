import pyautogui
import cv2
import time
import os
import threading
import pynput
import ctypes
class Recognize:

    def __init__(self):
        self.x=-1
        self.y=-1
        self.sa=0 #获取到坐标的个数
        self.sb=1 #执行完操作的个数
        self.end=False#外部函数操控内部图象识别是否停止的变量
        self.real=False#是否捕获到目标
        self.source_path = __file__[0:__file__.find("Game-Assistant")]
        self.resolutionRatio=pyautogui.size()

    def pa(self):
        self.sa-=1
        while self.sa<0:
            time.sleep(0.2)

    def pb(self):
        self.sb-=1
        while self.sb<0:
            time.sleep(0.2)

    def va(self):
        self.sa+=1

    def vb(self):
        self.sb+=1

    def ToRecongnizeIsHave(self,image_path,confidence=0.8):
        thread_a = threading.Thread(target=self.ToRecognizeConWhere, args=[self.source_path + "Game-Assistant\\Source\\" + str(self.resolutionRatio[0]) + "TestSpeak1.png", ])
        thread_a.start()
        stop = 0
        while True:
            self.pa()
            if not thread_a.is_alive():
                return
            if self.real:
                self.end=True
                return True
            else:
                """
                识别不到的停止机制如果连续10次识别不到那么终止
                """
                stop += 1
                if stop > 3:
                    self.end = True
                    return False
            self.vb()

    def ToRecognizeWhere(self,image_path,confidence=0.8):
        """
        用来识别特定图像是否存在,若存在返回其位置
        如果不存在返回False
        :param image_path: 图像存储位置
        :param confidence: 置信度识别不到调低一点一般都是0.8改低了容易识别到其他位置
        :return: 坐标(通过self.x和self.y)True或False
        """
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location is not None:
                self.x,self.y = pyautogui.center(location)
                return True
            else:
                return False
        except Exception :
            return False

    def ToRecognizeConWhere(self,image_path,confidence=0.8):
        """
        持续识别一个图像终止条件是将self.end设置为True(所以一个Recognize只能使用一个这样的函数不然会导致参数混乱)
        使用pa()来等待图像识别返回坐标,利用完返回完的坐标执行完操作使用vb()继续得到坐标
        每次返回坐标有可能是空坐标,self.real为真表示返回的是真坐标,连续返回多次假坐标可以考虑利用self.end关闭线程
        每次调用此函数需新建一个线程,记得启动线程
        :param image_path:
        :param confidence:置信度尽量别动
        :return:停止时返回False基本没用
        """
        while True:
            try:
                self.pb()
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location is not None:
                    self.x, self.y = pyautogui.center(location)
                    self.real=True
                    self.va()
                else:
                    return False
            except Exception as e:
                self.va()
                if self.end:
                    return False



    def ToRecognizeIfThen(self,image_path,Fuction,confidence=0.8):
        """
        用来识别图像是否存在,若不存在一直识别,直到存在执行Fuction(location,self)
        location是坐标,self返回这个类的对象,方便调用self.end来关闭正在一直识别的那个函数
        比如我一直识别感叹号然后还加了一个一直识别交互按钮的线程我将交互按钮放到这个函数里一旦识别到交互按钮我就将识别感叹号的函数关掉
        Function需自己提供,根据不同场景自己设置
        :param image_path:
        :param Fuction: 自己提供的函数
        :param confidence:
        :return:
        """
        while True:
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location is not None:
                    Fuction(location,self)
                    return
                else:
                    time.sleep(0.2)
            except Exception as e:
                time.sleep(0.2)

    def trakingImage(self,image_path,confidence=0.8):
        """
        通过调用ToRecognizeConWhere来实现图像追d踪(比较强大)
        通过self.end关闭
        :param image_path:
        :param confidence:
        :return:
        """
        thread_a = threading.Thread(target=self.ToRecognizeConWhere, args=[image_path,confidence])
        thread_a.start()
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        keyboard = pynput.keyboard.Controller()
        while True:
            self.pa()
            if  not thread_a.is_alive():
                return False
            if self.real:
                ctypes.windll.user32.mouse_event(0x0001, ctypes.c_int(int((self.x-center_x)/2)),0)
            else:
                self.vb()
                continue
            keyboard.press('w')
            time.sleep(1)
            keyboard.release('w')
            self.vb()

    # def click_image(self, image_path):
    #     try:
    #         location = pyautogui.locateOnScreen(image_path, confidence=0.7)
    #         if location is not None:
    #             x, y = pyautogui.center(location)  # 获取图像中心坐标
    #             pyautogui.click(x, y)  # 点击图像中心位置
    #     except Exception as e:
    #         return False

rec=Recognize()


