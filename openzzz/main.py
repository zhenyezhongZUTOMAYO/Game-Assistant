import pyautogui
import pynput
from time import sleep
def openZzz():
    keyboard=pynput.keyboard.Controller()
    sleep(4)
    keyboard.press(pynput.keyboard.Key['f2'])
    sleep(0.5)
    keyboard.release(pynput.keyboard.Key['f2'])
    pyautogui.click(1819,197)#(x,y)作战
    sleep(1)
    pyautogui.click(442,618)#(x,y)零号空洞
    sleep(1)
    pyautogui.click(1939,631)#(x,y)前往
    sleep(1)
    pyautogui.click(1459,826)#(x,y)确认
    sleep(3)
    pyautogui.click(1750,789)#(x,y)战线肃清
    sleep(1)
    pyautogui.click(1750,789)#(x,y)点一个buff
    sleep(1)
    pyautogui.click(2274,1372)#(x,y)下一步
    sleep(1)
    pyautogui.click(2274,1372)#(x,y)出战
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






