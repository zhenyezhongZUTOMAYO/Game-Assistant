from time import sleep
import Recognize
import pyautogui
import threading
import time
import os
import sys


class BuffSelector:
    def __init__(self):
        self.rec = Recognize.Recognize()
        self.running = False
        self.current_mode = None
        self.thread = None

        # 模式配置
        self.modes_config = {
            "BloodLoss": {
                "entry_image": self._get_image_path("BloodLoss.png"),
                "actions": [
                    {"image": self._get_image_path("BloodLoss.png"), "name": "选择流血buff", "delay": 1},
                ],
                "exit_image": self._get_image_path("Confirm.png"),
                "cooldown": 2  # 模式执行后的冷却时间
            },
            "Lottery": {
                "entry_image": self._get_image_path("Lottery.png"),
                "actions": [
                    {"image": self._get_image_path("Lottery.png"), "name": "抽奖", "delay": 1},
                ],
                "exit_image": self._get_image_path("ExitLottery.png"),
                "cooldown": 2
            },
            "RandomBuff": {
                "entry_image": self._get_image_path("Buff.png"),
                "actions": [
                    {"image": self._get_image_path("Buff.png"), "name": "选择buff", "delay": 1},
                ],
                "exit_image": self._get_image_path("Confirm.png"),
                "cooldown": 2
            }
        }
        # 验证所有图片文件是否存在
        self._validate_image_files()

    def _get_image_path(self, filename):
        """获取图片完整路径"""
        return os.path.join("E:\\GitHub\\Game-Assistant\\Source", filename)

    def _validate_image_files(self):
        """验证所有配置的图片文件是否存在"""
        missing_files = []

        for mode, config in self.modes_config.items():
            # 检查入口图片
            if not os.path.exists(config["entry_image"]):
                missing_files.append(config["entry_image"])

            # 检查动作图片
            for action in config["actions"]:
                if not os.path.exists(action["image"]):
                    missing_files.append(action["image"])

            # 检查退出图片
            if not os.path.exists(config["exit_image"]):
                missing_files.append(config["exit_image"])

        if missing_files:
            print("错误: 以下图片文件缺失:")
            for file in missing_files:
                print(f"- {file}")
            sys.exit(1)

    def _execute_mode_actions(self, mode_config):
        """执行指定模式的动作序列"""
        print(f"[模式激活] {self.current_mode}")

        for action in mode_config["actions"]:
            print(f"等待执行: {action['name']}")
            start_time = time.time()

            while self.running and time.time() - start_time < 10:  # 最多等待10秒

                # 检测目标图片
                if self.rec.ToRecognizeWhere(action["image"]):
                    print(f"执行 {action['name']} 位置: ({self.rec.x}, {self.rec.y})")
                    pyautogui.click(self.rec.x, self.rec.y)
                    time.sleep(action["delay"])
                    break

                # 优先检查退出条件
                if self.rec.ToRecognizeWhere(mode_config["exit_image"]):
                    print("检测到退出确认，点击确认")
                    pyautogui.click(self.rec.x, self.rec.y)
                    return True

                time.sleep(0.2)

            else:
                print(f"超时: 未找到 {action['name']} 图片")
                return False

        # 最后确认退出
        if self.rec.ToRecognizeWhere(mode_config["exit_image"]):
            pyautogui.click(self.rec.x, self.rec.y)

        print(f"[模式完成] {self.current_mode}")
        return True

    def _mode_detection_loop(self):
        """模式检测主循环"""
        last_mode_time = 0

        while self.running:
            current_time = time.time()

            # 检查冷却时间
            if current_time - last_mode_time < 1:  # 全局1秒冷却
                time.sleep(0.1)
                continue

            # 检测所有可能的模式
            for mode_name, config in self.modes_config.items():
                # 检查模式特定的冷却时间
                if self.current_mode == mode_name and current_time - last_mode_time < config["cooldown"]:
                    continue

                if self.rec.ToRecognizeWhere(config["entry_image"]):
                    self.current_mode = mode_name
                    if self._execute_mode_actions(config):
                        last_mode_time = time.time()
                    break

            time.sleep(0.2)

    def start(self):
        """启动检测线程"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._mode_detection_loop, daemon=True)
            self.thread.start()
            print("Buff选择器已启动")

    def stop(self):
        """停止检测"""
        if self.running:
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join()
            print("Buff选择器已停止")


def main():
    selector = BuffSelector()
    selector.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        selector.stop()
        print("程序已安全退出")


if __name__ == "__main__":
    main()