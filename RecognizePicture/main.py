import Recognize
import ctypes
import sys
from Recognize import rec
import pynput
import pyautogui
import threading
import time

def method(location):
    keyboard = pynput.keyboard.Controller()
    keyboard.press('f')
    time.sleep(0.5)
    keyboard.release('f')
    Speak()

def Speak():
    rec =Recognize.Recognize()
    thread_a = threading.Thread(target=rec.ToRecognizeConWhere, args=[rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio)+"TestSpeak1.png",])
    thread_a.start()
    while True:
        rec.pa()
        if not thread_a.is_alive():
            return
        clickMethod(rec.x,rec.y)
        rec.vb()

def is_admin():
    """检查当前是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """以管理员权限重新运行程序"""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None,  # 父窗口句柄
            "runas",  # 请求管理员权限
            sys.executable,  # 当前 Python 解释器路径
            " ".join(sys.argv),  # 命令行参数
            None,  # 工作目录
            0  # 显示窗口
        )



def clickMethod(x,y):
    pyautogui.click(x, y)  # 点击图像中心位置


def CommunicateToNpc(confidence=0.8):
    # thread_a=threading.Thread(target=rec.ToRecognizeConWhere,args=[rec.source_path+"GanTan.png",])
    thread_b=threading.Thread(target=rec.ToRecognizeIfThen , args=[rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio)+"Inter.png",method,confidence])
    # thread_a.start()
    thread_b.start()
    rec.trakingImage(rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio)+"GanTan.png",confidence)
    # screen_width, screen_height =pyautogui.size()
    # center_x=screen_width // 2
    # center_y=screen_height // 2
    # keyboard=pynput.keyboard.Controller()
    # while True:
    #     rec.pa()
    #     ctypes.windll.user32.mouse_event(0x0001,center_x-rec.x,center_y-rec.y)
    #     keyboard.press('w')
    #     time.sleep(2)
    #     keyboard.release('w')
    #     rec.vb()
    # thread_c=threading.Thread(target=rec.ToRecognizeIfThen,args=[rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio)+"TestSpeak1.png" , clickMethod,confidence])
    # thread_d=threading.Thread(target=rec.ToRecognizeIfThen,args=[rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio)+"TestSpeak2.png" , clickMethod,confidence])
    # thread_c.start()
    # thread_d.start()
    #点击对话箭头（上面两行）
if __name__=="__main__":
    # if not is_admin():
    #     run_as_admin()
    #     sys.exit()  # 退出当前非管理员权限的进程
    # openzzz.openZzz()
    rec.ToRecognizeIfThen(rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio)+"GanTan.png",CommunicateToNpc())

