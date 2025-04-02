import pyautogui
import pynput
from time import sleep

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

def openZzz():
    original_res=(2560,1440)
    target_res=pyautogui.size()
    size_t=0
    if target_res[0]/target_res[1]!=16/9:
        size_t=(target_res[1]-target_res[0]/16*9)/2
    # pyautogui.click(convert_coordinates(100, 100, original_res, target_res))  # 第一次登录点击
    # sleep(1)
    # pyautogui.click(convert_coordinates(100, 100, original_res, target_res))  # 第二次登录点击
    # sleep(1)
    keyboard=pynput.keyboard.Controller()
    keyboard.press(pynput.keyboard.Key['f2'])
    sleep(0.5)
    keyboard.release(pynput.keyboard.Key['f2'])
    # sleep(2)
    # pyautogui.press('f2')  # 替代 pynput 的键盘控制
    # sleep(2)
    pyautogui.click(convert_coordinates(1819,197,original_res,target_res))#(x,y)作战
    sleep(1)
    pyautogui.click(convert_coordinates(442,618,original_res,target_res))#(x,y)零号空洞
    sleep(1)
    pyautogui.click(convert_coordinates(1939,631,original_res,target_res))#(x,y)前往
    sleep(1)
    pyautogui.click(convert_coordinates(1459,826,original_res,target_res))#(x,y)确认
    sleep(3)
    pyautogui.click(convert_coordinates(1750,789-size_t,original_res,target_res))#(x,y)战线肃清
    sleep(1)
    pyautogui.click(convert_coordinates(1750,789-size_t,original_res,target_res))#(x,y)点一个buff
    sleep(1)
    pyautogui.click(convert_coordinates(2274,1372-size_t,original_res,target_res))#(x,y)下一步
    sleep(1)
    pyautogui.click(convert_coordinates(2274,1372-size_t,original_res,target_res))#(x,y)出战
    
if __name__=="__main__":
    # keyboard = pynput.keyboard.Controller()
    # keyboard.press(pynput.keyboard.Key.f2)
    # sleep(0.5)
    # keyboard.release(pynput.keyboard.Key.f2)
    openZzz()
# pyautogui.keyUp('alt')

# def on_click(x, y, button, pressed):
#     if pressed:  # 只在按下鼠标时触发
#         print(f"鼠标点击坐标: ({x}, {y})")  # 点击后输出坐标
#
# if __name__ == "__main__":
#
#     print("开始监听鼠标点击，按 Ctrl+C 退出...")
#
#     # 创建鼠标监听器
#     listener = mouse.Listener(on_click=on_click)
#
#     # 启动监听器
#     listener.start()
#
#     # 保持程序运行
#     try:
#         while True:
#             # 实时显示鼠标位置（不覆盖之前的输出）
#             x, y = pyautogui.position()
#             print(f"当前鼠标位置: ({x}, {y})", end="\r")  # \r 覆盖当前行
#     except KeyboardInterrupt:
#         print("\n程序结束")






