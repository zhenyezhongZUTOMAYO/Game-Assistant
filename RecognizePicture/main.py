import Recognize
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
    threading.Thread(target=rec.ToRecognizeConWhere,args=[source_path+"感叹号.png",])
    threading.Thread(target=rec.ToRecognizeIfThen , args=[source_path+"交互按钮.png",method])
    # screen_width, screen_height =pyautogui.size()
    # center_x=screen_width // 2
    # center_y=screen_height // 2
    keyboard=pynput.keyboard.Controller()
    while True:
        if rec.x!=-1 & rec.y!=-1:
            pyautogui.dragTo(rec.x,rec.y)
        keyboard.press('w')
        time.sleep(2)
        keyboard.release('w')
