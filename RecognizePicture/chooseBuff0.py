from time import sleep
import Recognize
import ctypes
from Recognize import rec
import pynput
import pyautogui
import threading
import time

# 初始化 Recognize 类
rec = Recognize.Recognize()

# 定义图片路径和优先级
PRIORITY_IMAGES = {
    "priority0": "E:\\GitHub\\Game-Assistant\\Soruce\\Buff0.png",  # 高优先级图片
    "priority10": "E:\\GitHub\\Game-Assistant\\Soruce\\Buff10.png",  # 中0优先级图片
    "priority11": "E:\\GitHub\\Game-Assistant\\Soruce\\Buff11.png",  # 中1优先级图片
    "priority12": "E:\\GitHub\\Game-Assistant\\Soruce\\Buff12.png",  # 中2优先级图片
    "priority13": "E:\\GitHub\\Game-Assistant\\Soruce\\Buff13.png",  # 中3优先级图片
    "priority2": "E:\\GitHub\\Game-Assistant\\Soruce\\Buff2.png",  # 低优先级图片
}

# 定义每种优先级的点击操作
def priority0_action(x, y):
    print(f"高优先级图片 detected! 点击位置: ({x}, {y})")
    pyautogui.click(x, y)  # 点击高优先级图片的位置

def priority10_action(x, y):
    print(f"中0优先级图片 detected! 点击位置: ({x}, {y})")
    pyautogui.click(x, y)  # 点击中1优先级图片的位置

def priority11_action(x, y):
    print(f"中1优先级图片 detected! 点击位置: ({x}, {y})")
    pyautogui.click(x, y)  # 点击中1优先级图片的位置

def priority12_action(x, y):
    print(f"中2优先级图片 detected! 点击位置: ({x}, {y})")
    pyautogui.click(x, y)  # 点击中2优先级图片的位置

def priority13_action(x, y):
    print(f"中3优先级图片 detected! 点击位置: ({x}, {y})")
    pyautogui.click(x, y)  # 点击中3优先级图片的位置

def priority2_action(x, y):
    print(f"低优先级图片 detected! 点击位置: ({x}, {y})")
    pyautogui.click(x, y)  # 点击低优先级图片的位置

# 优先级对应的操作函数
PRIORITY_ACTIONS = {
    "priority0": priority0_action,
    "priority10": priority10_action,
    "priority11": priority11_action,
    "priority12": priority12_action,
    "priority13": priority13_action,
    "priority2": priority2_action,
}

def detect_priority(priority, image_path, action_func):
    """
    检测指定优先级图片的线程函数。
    :param priority: 优先级名称（用于日志）
    :param image_path: 图片路径
    :param action_func: 点击操作函数
    """
    print(f"启动线程: {priority}, 图片路径: {image_path}")  # 调试输出
    while True:
        print(f"检测图片: {image_path}")  # 调试输出
        if rec.ToRecognizeWhere(image_path):
            print(f"找到图片: {image_path}, 坐标: ({rec.x}, {rec.y})")  # 调试输出
            action_func(rec.x, rec.y)  # 执行点击操作
            time.sleep(1)  # 点击后等待 1 秒，避免重复点击
        else:
            print(f"未找到图片: {image_path}")  # 调试输出
            time.sleep(0.2)  # 未检测到图片时，短暂等待

def main():
    # 启动多个线程，分别检测不同优先级的图片
    threads = []
    for priority, image_path in PRIORITY_IMAGES.items():
        print(f"创建线程: {priority}, 图片路径: {image_path}")  # 调试输出
        thread = threading.Thread(
            target=detect_priority,
            args=(priority, image_path, PRIORITY_ACTIONS[priority]),
        )
        thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        thread.start()
        threads.append(thread)

    # 主线程保持运行
    try:
        while True:
            time.sleep(1)  # 主线程保持运行，防止程序退出
    except KeyboardInterrupt:
        print("程序已退出。")

if __name__ == "__main__":
    sleep(3)  # 等待 3 秒，确保程序启动后有时间切换到目标窗口
    main()