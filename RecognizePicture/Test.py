import pyautogui
import ctypes
import sys
import time
import Recognize
import SpeakNpc
from main import  *

import cv2
import numpy as np

def locate_with_alpha(template_path, confidence=0.8):
    """
    匹配带透明通道的图片
    :param template_path: 模板图片路径（PNG 透明背景）
    :param confidence: 匹配阈值（0~1）
    :return: 匹配位置 (left, top, width, height)，或 None
    """
    # 1. 读取模板图片（带 Alpha 通道）
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)  # BGRA 格式
    template_bgr = template[:, :, :3]  # BGR 部分
    template_alpha = template[:, :, 3]  # Alpha 通道
    mask = cv2.threshold(template_alpha, 1, 255, cv2.THRESH_BINARY)[1]  # 非透明部分=255

    # 2. 获取屏幕截图（BGR 格式）
    screenshot = np.array(pyautogui.screenshot())
    screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # RGB -> BGR

    # 3. 执行模板匹配（仅匹配非透明部分）
    result = cv2.matchTemplate(screenshot_bgr, template_bgr, cv2.TM_CCOEFF_NORMED, mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= confidence:
        h, w = template_bgr.shape[:2]
        return (*max_loc, w, h)  # (left, top, width, height)
    else:
        return None

# 示例用法


def Test(rec):
    """

    :param rec:
    :return:
    测试rec在函数内部能不能修改
    """
    rec.end=True

def detectGanTanHao():
    # Speak()
    # CommunicateToNpc(0.8)
    # rec=Recognize.Recognize()
    # print(rec.end)
    # Test(rec)
    # print(rec.end)

    # 获取当前文件夹路径

    # print("当前文件夹路径:", __file__)
    # print(__file__[0:__file__.find("Game-Assistant")-1])
    # ctypes.windll.user32.mouse_event(0x0001, 100,100)
    #method()正常
    # CommunicateToNpc()
    # rec.trakingImage(rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio)+"GanTan.png",0.3)
    # rec.ToRecognizeIfThen("D:\\Git\\Game-Assistant\\Source\\Inter.png",method)
    # 等待一段时间，方便你切换到目标屏幕
    # screen_width, screen_height = pyautogui.size()
    # center_x = screen_width // 2
    # center_y = screen_height // 2
    # rec.ToRecognizeConWhere("D:\\Git\\Game-Assistant\\Source\\GanTan.png")
    # time.sleep(1)
    # pyautogui.moveRel(960,0,duration=0.5)
    #指定要查找的图片路径
    image_path = rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "GanTan.png"

    try:
        # 在屏幕上查找图片
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)

        if location is not None:
            # 获取图片的中心坐标
            x1, y1 = pyautogui.center(location)
            print(f"找到图片，坐标位于: ({x1}, {y1})")
        else:
            print("未找到图片")
    except Exception as e:
        print(f"发生错误: {e}")

    image_path_1 = rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "GanTanSpeak.png"

    try:
        # 在屏幕上查找图片
        location = pyautogui.locateOnScreen(image_path_1, confidence=0.8)

        if location is not None:
            # 获取图片的中心坐标
            x2, y2 = pyautogui.center(location)
            print(f"找到图片，坐标位于: ({x2}, {y2})")
        else:
            print("未找到图片")
    except Exception as e:
        print(f"发生错误: {e}")
    print(f"({x2-x1},{y2-y1})")

if __name__=="__main__":
    # time.sleep(2)
    # spk=SpeakNpc.SpeakNpc()
    # spk.isBuff()
    detectGanTanHao()
    # match_pos = locate_with_alpha("D:\\Git\\Game-Assistant\\Source\\3840GanTan111.png", confidence=0.8)
    # if match_pos:
    #     x, y, w, h = match_pos
    #     print(f"匹配成功！位置：{x + w // 2},{y + h // 2}")
    #        # 点击中心
    # else:
    #     print("匹配失败！")
    # rec=Recognize.Recognize()
    # now=time.time()
    # rec.ToRecongnizeIsHave("D:\\Git\\Game-Assistant\\Source\\2560GanTan.png")
    # then=time.time()
    # print(then-now)