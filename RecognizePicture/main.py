import Recognize
import ctypes
import sys
from EnterNextLevel import  LevelSystem
from Recognize import rec
import pynput
import pyautogui
import threading
import time
import ChooseBuff
import GanTanChat
import SumRecognize
def method(location,rec):
    keyboard = pynput.keyboard.Controller()
    keyboard.press('f')
    time.sleep(0.5)
    keyboard.release('f')
    rec.end=True
    Speak()
    keyboard.press('s')
    time.sleep(2)
    keyboard.release('s')

def Speak():
    """
    这是一个与人对话的函数如果2秒内未出现与人交流的白点那么退出识别
    :return: None
    """
    rec =Recognize.Recognize()
    thread_a = threading.Thread(target=rec.ToRecognizeConWhere, args=[rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio[0])+"TestSpeak1.png",])
    thread_a.start()
    stop=0
    while True:
        rec.pa()
        if not thread_a.is_alive():
            return
        if rec.real:
            pyautogui.click(rec.x,rec.y)
            stop=0
        else:
            """
            识别不到的停止机制如果连续10次识别不到那么终止
            """
            stop+=1
            if stop > 3:
                rec.end=True
        rec.vb()

# def is_admin():
#     """检查当前是否以管理员权限运行"""
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False
#
# def run_as_admin():
#     """以管理员权限重新运行程序"""
#     if not is_admin():
#         ctypes.windll.shell32.ShellExecuteW(
#             None,  # 父窗口句柄
#             "runas",  # 请求管理员权限
#             sys.executable,  # 当前 Python 解释器路径
#             " ".join(sys.argv),  # 命令行参数
#             None,  # 工作目录
#             0  # 显示窗口
#         )
"""
上面这个申请管理员权限先别用
因为这个是用当前进程创建新的进程新的进程用管理员权限运行然后杀掉老的进程但是我这个没给他设置运行窗口就导致你调试完不知道还有几个进程在跑CPU占用率就会非常高但是显卡占用率不怎么高
所以之后就是用统一的一个C++进程来用管理员权限启动python程序这样的话一个C++进程管理一个python进程就不会乱也可以直接生成exe文件运行
"""





def CommunicateToNpc(confidence=0.8):
    # thread_a=threading.Thread(target=rec.ToRecognizeConWhere,args=[rec.source_path+"GanTan.png",])

    thread_b=threading.Thread(target=rec.ToRecognizeIfThen , args=[rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio[0])+"Inter.png",method,confidence])
    # thread_a.start()
    thread_b.start()
    rec.trakingImage(rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio[0])+"GanTan.png",confidence)
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
    # thread_c=threading.Thread(target=rec.ToRecognizeIfThen,args=[rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio[0])+"TestSpeak1.png" , pyautogui.click,confidence])
    # thread_d=threading.Thread(target=rec.ToRecognizeIfThen,args=[rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio[0])+"TestSpeak2.png" , pyautogui.click,confidence])
    # thread_c.start()
    # thread_d.start()
    #点击对话箭头（上面两行）
if __name__=="__main__":
    # if not is_admin():
    #     run_as_admin()
    #     sys.exit()  # 退出当前非管理员权限的进程
    # openzzz.openZzz()
    # buff = ChooseBuff.BuffSelector()
    # buff.start()
    # gantan=GanTanChat.GanTanChat()
    # gantan.BuffSelector=buff
    # rec.ToRecognizeIfThen(rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio[0])+"GanTan.png",gantan.CommunicateToNpc())
    # rec.ToRecognizeIfThen(rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "GanTan.png",gantan.CommunicateToNpc())
    sum=SumRecognize.SumRecognize()
    sum.start()
    # thread=[]
    # sum.lock[0]=1
    # thread_yd = threading.Thread(target=sum.YuanDian,)
    # thread.append(thread_yd)
    # for thr in thread:
    #     thr.start()
    # for thr in thread:
    #     thr.join()
    # sum.lock[0]=1
    # sum.yd.trackingYuanDian(sum.lock)

    # sum.lock[0]=1
    # sum.YuanDian()
    # rec.trakingImage(rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio[0])+"Direction.png")
    #level_system = LevelSystem()  # 创建进入下一层实例
    #level_system.start()  # 开始检测入口
