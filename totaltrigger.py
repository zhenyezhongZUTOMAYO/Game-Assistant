import time
import threading
import os
from RecognizePicture.EnterNextLevel import LevelSystem
from RecognizePicture.GanTanChat import GanTanChat
from openzzz.main import openZzz

class TotalTrigger:
    def __init__(self):
        self.level_system = LevelSystem()
        self.chat_system = GanTanChat()
        self.lock = [1, 1]  # 第一个锁用于对话系统，第二个锁用于传送门系统
        
    def start_game(self):
        """启动游戏并进行准备"""
        print("开始启动游戏...")
        openZzz()
        print("游戏启动完成")
        
    def start_chat(self):
        """启动对话系统"""
        print("启动对话系统...")
        self.chat_system.start(self.lock)
        
    def start_level_system(self):
        """启动传送门系统"""
        print("启动传送门系统...")
        self.level_system.start(self.lock)
        
    def start(self):
        """启动所有系统"""
        try:
            # 启动游戏
            self.start_game()
            
            # 等待游戏加载
            time.sleep(5)
            
            # 创建并启动对话系统线程
            chat_thread = threading.Thread(target=self.start_chat)
            chat_thread.start()
            
            # 创建并启动传送门系统线程
            level_thread = threading.Thread(target=self.start_level_system)
            level_thread.start()
            
            # 保持主线程运行
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("程序退出")
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    trigger = TotalTrigger()
    trigger.start() 