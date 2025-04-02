import time
import threading
import os
from RecognizePicture.SumRecognize import SumRecognize
from openzzz.main import openZzz

class TotalTrigger:
    def __init__(self):
        self.sumr=SumRecognize()

    def logInGame(self):
        pass

    def start_game(self):
        """启动游戏并进行准备"""
        print("开始启动游戏...")
        openZzz()
        print("游戏启动完成")

        
    def start(self):
        """启动所有系统"""
        try:
            # 启动游戏
            self.start_game()
            self.sumr.start()
        except KeyboardInterrupt:
            print("程序退出")

if __name__ == "__main__":
    trigger = TotalTrigger()
    trigger.start() 