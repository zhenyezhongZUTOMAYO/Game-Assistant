import pyautogui
import pynput
import cv2
import time
# pyautogui.moveTo(84,201)
start = time.time()
image_path = "D:\\Git\\Game-Assistant\\Soruce\\TestPicture.png"
try:

    location = pyautogui.locateOnScreen(image_path, confidence=0.8)

    if location is not None:
        # 获取图片的中心坐标
        x, y = pyautogui.center(location)
        end=time.time()
        print(f"用时{end-start}")
        print(f"找到图片，坐标位于: ({x}, {y})")
    else:
        print("未找到图片")
except Exception as e:
    print(f"发生错误: {e}")