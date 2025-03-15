import Recognize
import ctypes
from Recognize import rec
import pynput
import pyautogui
import threading
import time

def method():
    keyboard = pynput.keyboard.Controller()
    keyboard.press('f')
    time.sleep(0.5)
    keyboard.release('f')

source_path = "D:\\Git\\Game-Assistant\\Soruce\\"
def CommunicateToNpc():
    # thread_a=threading.Thread(target=rec.ToRecognizeConWhere,args=[source_path+"GanTan.png",])
    thread_b=threading.Thread(target=rec.ToRecognizeIfThen , args=[source_path+"Inter.png",method])
    # thread_a.start()
    thread_b.start()
    rec.trakingImage("D:\\Git\\Game-Assistant\\Soruce\\GanTan.png")
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
    thread_c=threading.Thread(target=rec.ToRecognizeIfThen,args=["D:\\Git\\Game-Assistant\\Soruce\\TestSpeak1.png" , lambda: rec.click_image("D:\\Git\\Game-Assistant\\Soruce\\Speak1.png"),])
    thread_d=threading.Thread(target=rec.ToRecognizeIfThen,args=["D:\\Git\\Game-Assistant\\Soruce\\TestSpeak2.png" , lambda: rec.click_image("D:\\Git\\Game-Assistant\\Soruce\\Speak2.png"),])
    thread_c.start()
    thread_d.start()
    #点击对话箭头（上面两行）
if __name__=="__main__":
    time.sleep(3)
    CommunicateToNpc()
