import time
import pynput
import pyautogui
import os
from Recognize import Recognize


class LevelSystem:
    def __init__(self):
        self.rec = Recognize()  # 独立实例
        self.keyboard = pynput.keyboard.Controller()
        self.confidence = 0.3  # 确保拼写正确，并且有默认值

    def _method(self, location, _):
        import pyautogui

        # 先点击目标位置确保焦点
        center_x = location.left + location.width // 2
        center_y = location.top + location.height // 2
        pyautogui.click(center_x, center_y)

        # 发送按键
        pyautogui.press('f')
        print("?? 已通过pyautogui发送F键")
        self._enter_flow()

    def start_detection(self):
        """直接调用核心功能（非线程模式）"""
        # 使用os.path.join安全拼接路径
        image_path = os.path.join(
            self.rec.source_path,
            "Game-Assistant",
            "Source",
            f"{self.rec.resolutionRatio[0]}levelEntrance.png"
        )

        # 调试信息
        print(f"完整图片路径: {image_path}")
        print(f"文件是否存在: {os.path.exists(image_path)}")

        # 直接调用识别功能（不再使用线程）
        self.rec.ToRecognizeIfThen(image_path, self._method, self.confidence)

        # 直接调用跟踪功能
        self.rec.trakingImage(image_path, self.confidence)

    def _enter_flow(self):
        print("进入_enter_flow流程")
        timeout = time.time() + 30  # 30秒超时机制
        stop = 0

        while time.time() < timeout:
            self.rec.pa()
            print(f"当前状态: real={self.rec.real} | 坐标({self.rec.x},{self.rec.y}) | 累计失败{stop}次")  # 新增

            if self.rec.real:
                print(f"执行点击: ({self.rec.x}, {self.rec.y})")
                pyautogui.click(self.rec.x, self.rec.y)
                stop = 0
            else:
                stop += 1
                if stop > 9:
                    print("达到最大失败次数，退出流程")
                    return

            time.sleep(0.5)  # 降低CPU占用

        print("流程超时自动退出")
    def start(self):
        """模块启动入口"""
        print("程序启动")
        self.start_detection()
        try:
            while True:  # 保持主线程运行
                time.sleep(1)
        except KeyboardInterrupt:
            print("程序退出")


if __name__ == "__main__":
    system = LevelSystem()
    system.start()