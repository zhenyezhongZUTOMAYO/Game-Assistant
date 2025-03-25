from time import sleep
import Recognize
import pyautogui
import threading
import time
import os

# 初始化 Recognize 类
rec = Recognize.Recognize()

# 定义模式配置
MODES_CONFIG = {
    "BloodLoss": {
        "entry_image": "E:\\GitHub\\Game-Assistant\\Source\\BloodLoss.png",
        "actions": [
            {"image": "E:\\GitHub\\Game-Assistant\\Source\\BloodLoss.png", "name": "动作", "delay": 1},
        ],
        "exit_image": "E:\\GitHub\\Game-Assistant\\Source\\Confirm.png"
    },
    "mode2": {
        "entry_image": "E:\\GitHub\\Game-Assistant\\Source\\ChooseOne.png",
        "actions": [
            {"image": "E:\\GitHub\\Game-Assistant\\Source\\Buff.png", "name": "动作", "delay": 1},
        ],
        "exit_image": "E:\\GitHub\\Game-Assistant\\Source\\Confirm.png"
    }
}


class ModeExecutor:
    def __init__(self):
        self.current_mode = None
        self.running = True

    def execute_action_sequence(self, mode_config):
        """按顺序执行模式下的动作"""
        print(f"开始执行模式: {self.current_mode}")

        for action in mode_config["actions"]:
            print(f"等待执行: {action['name']}")
            while self.running:
                # 检查是否需要退出当前模式
                if rec.ToRecognizeWhere(mode_config["exit_image"]):
                    print("检测到退出条件，终止当前模式")
                    pyautogui.click(rec.x, rec.y)
                    return

                if rec.ToRecognizeWhere(action["image"]):
                    print(f"执行 {action['name']} 在位置: ({rec.x}, {rec.y})")
                    pyautogui.click(rec.x, rec.y)
                    time.sleep(action["delay"])  # 执行后等待
                    break
                time.sleep(0.2)

        print(f"完成模式: {self.current_mode}")

    def detect_and_execute_modes(self):
        """检测并执行各种模式"""
        while self.running:
            for mode, config in MODES_CONFIG.items():
                if rec.ToRecognizeWhere(config["entry_image"]):
                    self.current_mode = mode
                    self.execute_action_sequence(config)
                    break
            time.sleep(0.5)

    def stop(self):
        """停止所有操作"""
        self.running = False


def main():
    executor = ModeExecutor()

    # 启动模式检测和执行线程
    mode_thread = threading.Thread(target=executor.detect_and_execute_modes)
    mode_thread.daemon = True
    mode_thread.start()

    # 主线程保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        executor.stop()
        print("程序已安全退出。")


if __name__ == "__main__":
    sleep(3)  # 等待3秒，确保程序启动后有时间切换到目标窗口
    main()