import cv2
import numpy as np
import pyautogui
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置检测间隔时间（秒）
CHECK_INTERVAL = 1

# 设置屏幕变化的阈值（像素差异总和）
THRESHOLD = 100000000

def capture_screen():
    """截取屏幕截图并转换为灰度图像"""
    screenshot = pyautogui.screenshot()  # 截取屏幕
    screenshot = np.array(screenshot)    # 转换为NumPy数组
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # 转换为灰度图像
    return screenshot

def compare_images(img1, img2):
    """比较两张图像的差异，返回差异值"""
    diff = cv2.absdiff(img1, img2)  # 计算差异
    diff_sum = np.sum(diff)         # 计算差异的总和
    return diff_sum

def main():
    print("开始检测屏幕是否几乎不动...")
    prev_screen = capture_screen()  # 获取初始屏幕截图

    while True:
        time.sleep(CHECK_INTERVAL)  # 等待一段时间
        current_screen = capture_screen()  # 获取当前屏幕截图

        # 比较两张截图
        diff_sum = compare_images(prev_screen, current_screen)
        print(f"屏幕差异值: {diff_sum}")

        if diff_sum < THRESHOLD:
            print("屏幕几乎不动！")
        else:
            print("屏幕内容发生变化。")

        prev_screen = current_screen  # 更新前一张截图

if __name__ == "__main__":
    main()