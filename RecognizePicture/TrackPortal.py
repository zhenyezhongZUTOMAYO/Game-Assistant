import time
import Recognize
import pyautogui
import pynput
import threading
import os
import sys

class PortalTracker:
    def __init__(self):
        self.rec = Recognize.Recognize()
        self.running = False
        self.thread = None
        self.keyboard = pynput.keyboard.Controller()
        self.mouse = pynput.mouse.Controller()
        
        # 配置传送门相关的图片路径
        self.portal_config = {
            "portal_image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}Portal.png",
            "portal_entrance": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}PortalEntrance.png",
            "portal_exit": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}PortalExit.png"
        }
        
        # 验证图片文件
        self._validate_image_files()
        
    def _validate_image_files(self):
        """验证所有配置的图片文件是否存在"""
        missing_files = []
        
        for key, path in self.portal_config.items():
            if not os.path.exists(path):
                missing_files.append(path)
                
        if missing_files:
            print("错误: 以下传送门相关图片文件缺失:")
            for file in missing_files:
                print(f"- {file}")
            sys.exit(1)
            
    def start_tracking(self):
        """开始追踪传送门"""
        if self.running:
            print("追踪已经在运行中")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._track_portal)
        self.thread.start()
        print("开始追踪传送门")
        
    def stop_tracking(self):
        """停止追踪传送门"""
        if not self.running:
            print("追踪已经停止")
            return
            
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
        print("停止追踪传送门")
        
    def _track_portal(self):
        """传送门追踪的主要逻辑"""
        last_click_time = 0
        click_cooldown = 1.0  # 点击冷却时间（秒）
        
        while self.running:
            try:
                # 检查是否看到传送门
                if self.rec.ToRecognizeWhere(self.portal_config["portal_image"]):
                    current_time = time.time()
                    
                    # 检查是否在冷却时间内
                    if current_time - last_click_time >= click_cooldown:
                        # 获取传送门位置
                        portal_x, portal_y = self.rec.x, self.rec.y
                        
                        # 移动到传送门位置
                        self.mouse.position = (portal_x, portal_y)
                        time.sleep(0.2)  # 等待鼠标移动完成
                        
                        # 点击传送门
                        self.mouse.click(pynput.mouse.Button.left)
                        last_click_time = current_time
                        
                        print(f"点击传送门位置: ({portal_x}, {portal_y})")
                        
                        # 等待进入传送门
                        time.sleep(1.0)
                        
                        # 检查是否成功进入传送门
                        if self.rec.ToRecognizeWhere(self.portal_config["portal_entrance"]):
                            print("成功进入传送门")
                            # 等待传送完成
                            time.sleep(2.0)
                            
                            # 检查是否成功退出传送门
                            if self.rec.ToRecognizeWhere(self.portal_config["portal_exit"]):
                                print("成功退出传送门")
                                continue
                                
                # 短暂休眠以避免过度占用CPU
                time.sleep(0.1)
                
            except Exception as e:
                print(f"追踪过程中出现错误: {str(e)}")
                time.sleep(1.0)  # 发生错误时等待较长时间
                
    def is_running(self):
        """检查追踪是否正在运行"""
        return self.running

# 创建全局实例
portal_tracker = PortalTracker() 