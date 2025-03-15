import pyautogui
import ctypes
from main import  *

def detectGanTanHao():
    # ctypes.windll.user32.mouse_event(0x0001, 100,100)
    #method()正常
    # CommunicateToNpc()
    # rec.ToRecognizeIfThen("D:\\Git\\Game-Assistant\\Soruce\\Inter.png",method)
    # 等待一段时间，方便你切换到目标屏幕
    # screen_width, screen_height = pyautogui.size()
    # center_x = screen_width // 2
    # center_y = screen_height // 2
    # rec.ToRecognizeConWhere("D:\\Git\\Game-Assistant\\Soruce\\GanTan.png")
    # time.sleep(1)
    # pyautogui.moveRel(960,0,duration=0.5)
    #指定要查找的图片路径
    image_path = "D:\\Git\\Game-Assistant\\Soruce\\TestSpeak1.png"

    try:
        # 在屏幕上查找图片
        location = pyautogui.locateOnScreen(image_path, confidence=0.7)

        if location is not None:
            # 获取图片的中心坐标
            x, y = pyautogui.center(location)
            print(f"找到图片，坐标位于: ({x}, {y})")
        else:
            print("未找到图片")
    except Exception as e:
        print(f"发生错误: {e}")
        image_path = "D:\\Git\\Game-Assistant\\Soruce\\TestSpeak2.png"

    try:
        # 在屏幕上查找图片
        location = pyautogui.locateOnScreen(image_path, confidence=0.7)

        if location is not None:
            # 获取图片的中心坐标
            x, y = pyautogui.center(location)
            print(f"找到图片，坐标位于: ({x}, {y})")
        else:
            print("未找到图片")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__=="__main__":
    time.sleep(2)
    detectGanTanHao()