import random
import threading
import cv2
import numpy as np
import pyautogui
import time
import os
import sys
import pynput
import Recognize
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置检测间隔时间（秒）
CHECK_INTERVAL = 1

# 设置屏幕变化的阈值（像素差异总和）
# 这个值可以根据实际情况进行调整
THRESHOLD = 300000000

# 设置连续低差异值的次数阈值
STUCK_THRESHOLD = 8

class AvoidStick:
    def __init__(self):
        self.lock=[]
        self.skip=False
    def capture_screen(self):
        """截取屏幕截图并转换为灰度图像"""
        screenshot = pyautogui.screenshot()  # 截取屏幕
        screenshot = np.array(screenshot)    # 转换为NumPy数组
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # 转换为灰度图像
        return screenshot

    def compare_images(self,img1, img2):
        """比较两张图像的差异，返回差异值"""
        diff = cv2.absdiff(img1, img2)  # 计算差异
        diff_sum = np.sum(diff)         # 计算差异的总和
        return diff_sum

    def handle_stuck(self):
        """处理屏幕几乎不动的情况"""
        """重新选择路标，选择新的路径进行移动"""
        print("检测到撞墙，尝试脱离...")
        # 在这里添加处理逻辑，例如点击鼠标、发送键盘事件等
        print("检测到撞墙，尝试脱离...")
        keyboard = pynput.keyboard.Controller()
        keyboard_lock = threading.Lock()
        direction = random.choice(['left', 'right'])  # 随机选择方向
        keyboard.release('w')
        keyboard.press('s')
        time.sleep(0.5)
        keyboard.release('s')
        with keyboard_lock:#键盘加锁
            if direction == 'left':
                #print("向左移动 0.5 秒")
                keyboard.press('a')  # 按下左方向键
                time.sleep(0.5)
                keyboard.release('a')  # 释放左方向键
            else:
                #print("向右移动 0.5 秒")
                keyboard.press('d')  # 按下右方向键
                time.sleep(0.5)
                keyboard.release('d')  # 释放右方向键
        #print("尝试脱离完成")

    def Solve(self):
        while True:
            self.solve()
            while self.lock[0] > 0:
                print(f"防卡Sleep{self.lock}")
                time.sleep(1)

    def solve(self):
        prev_screen = self.capture_screen()  # 获取初始屏幕截图
        stuck_count = 0  # 初始化撞墙计数
        while self.lock[0]==0:
            time.sleep(CHECK_INTERVAL)  # 等待一段时间
            current_screen = self.capture_screen()  # 获取当前屏幕截图
            diff_sum = self.compare_images(prev_screen, current_screen)  # 比较两张截图的差异
            print(f"屏幕差异值: {diff_sum}")

            if diff_sum < THRESHOLD:  # 如果屏幕变化值低于阈值
                stuck_count += 1
                print("屏幕几乎不动，可能撞墙！")
                if stuck_count > STUCK_THRESHOLD or self.skip:  # 如果连续多次检测到撞墙
                    self.handle_stuck()  # 调用撞墙处理函数
                    self.skip=True
                    stuck_count = 0  # 重置撞墙计数
                    break
            else:
                self.skip=False
                stuck_count = 0  # 重置撞墙计数

            prev_screen = current_screen  # 更新前一帧截图



    def solvex(self):
        prev_screen=self.capture_screen()
        stuck_count=0
        time.sleep(CHECK_INTERVAL)
        current_screen=self.capture_screen()
        diff_sum = self.compare_images(prev_screen, current_screen)
        # print(f"屏幕差异值: {diff_sum}")
        if diff_sum<THRESHOLD:#屏幕变化阈值
            stuck_count+=1
            if stuck_count>STUCK_THRESHOLD:
                self.handle_stuck()
                stuck_count=0
        else:
            stuck_count=0
        prev_screen = current_screen





def main():
    print("开始检测屏幕是否几乎不动...")
    avoid=AvoidStick()
    prev_screen = avoid.capture_screen()  # 获取初始屏幕截图

    while True:
        time.sleep(CHECK_INTERVAL)  # 等待一段时间
        current_screen = avoid.capture_screen()  # 获取当前屏幕截图

        # 比较两张截图
        diff_sum = avoid.compare_images(prev_screen, current_screen)
        print(f"屏幕差异值: {diff_sum}")

        if diff_sum < THRESHOLD:
            print("屏幕几乎不动！")
        else:
            print("屏幕内容发生变化。")

        prev_screen = current_screen  # 更新前一张截图

if __name__ == "__main__":
    main()