import time
import threading
import sys
import os
import pyautogui
from time import sleep
from RecognizePicture.Recognize import rec
from RecognizePicture.SumRecognize import SumRecognize
from openzzz.main import openZzz
sys.path.append(os.path.dirname(os.path.abspath(__file__+"\\RecognizePicture")))

class TotalTrigger:
    def __init__(self):
        self.sumr=SumRecognize()
        self.signal=True

    def click(self):
        while self.signal:
            print("我在点击")
            pyautogui.click()
            time.sleep(1)

    def method(self,rec,location):
        self.signal=False
    def start_game(self):
        """启动游戏并进行准备"""
        time.sleep(5)
        print("进入")
        thread_a=threading.Thread(target=self.click)
        thread_a.start()
        rec.ToRecognizeIfThen(rec.source_path+"Game-Assistant\\Source\\"+str(rec.resolutionRatio[0])+"Start.png",self.method)
        time.sleep(2)
        openZzz()
        print("游戏启动完成")

        
    def start(self):
        """启动所有系统"""
        try:
            # 启动游戏
            self.start_game()
            # pyautogui.click(100, 100)  # 先点击一个安全位置确保窗口激活
            # sleep(1)
            self.sumr.lock[0]=0
            self.sumr.lock[1]=1
            self.sumr.start()
        except KeyboardInterrupt:
            print("程序退出")

if __name__ == "__main__":
    trigger = TotalTrigger()
    trigger.start() 