import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from time import sleep
import Recognize
import pyautogui
import pynput
import threading
import time




def convert_coordinates(x, y, original_res, target_res):
    """
    将坐标从原分辨率转换到目标分辨率
    :param x: 原坐标x
    :param y: 原坐标y
    :param original_res: 原分辨率 (width, height)
    :param target_res: 目标分辨率 (width, height)
    :return: 转换后的坐标 (new_x, new_y)
    """

    original_width, original_height = original_res
    target_width, target_height = target_res

    # 计算缩放比例
    scale_x = target_width / original_width
    scale_y = target_height / original_height

    # 转换坐标
    new_x = int(x * scale_x)
    new_y = int(y * scale_y)

    return new_x, new_y

class BuffSelector:
    def __init__(self):
        self.rec = Recognize.Recognize()
        self.running = False
        self.current_mode = None
        self.thread = None
        self.sa=0
        self.lock=[]
        self.the_end_complete = 0
        self.limit = 999
        self.WinStart=time.time()
        self.WinEnd=None

        # 模式配置
        self.modes_config = {
            "Start": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}StartBuff.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Start1.png","name": "选择战备buff1", "delay": 1,"max_attempts":6,"is_skip":True},
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Start2.png","name": "选择战备buff2", "delay": 1,"max_attempts":6},
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Start0.png","name": "确认携带","delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}ExitStart.png",
                "cooldown": 2  # 模式执行后的冷却时间
            },
            "Store": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Store.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Store.png", "name": "商店页面",
                     "delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}ExitStart.png",
                "cooldown": 2  # 模式执行后的冷却时间
            },
            "BloodStore": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}BloodStore.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}BloodStore.png", "name": "血量商店页面",
                     "delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}ExitStart.png",
                "cooldown": 2  # 模式执行后的冷却时间
            },
            "BloodLoss": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}BloodLoss.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}BloodLoss.png", "name": "选择流血buff", "delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Confirm.png",
                "cooldown": 2  # 模式执行后的冷却时间
            },
            "Lottery": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Lottery.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Lottery.png", "name": "抽奖", "delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}ExitLottery.png",
                "cooldown": 2
            },
            "GetGift": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}GetGift.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Buff.png", "name": "获得战利品",
                     "delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Confirm.png",
                "cooldown": 2
            },
            "GetGear": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}GetGear.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Gear.png", "name": "获得战备",
                     "delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Confirm.png",
                "cooldown": 2
            },
            "Gearup": {
                "entry_image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}Gearup.png",
                "actions": [
                    {"image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}Gearup.png","name": "战备升级","delay": 1},
                ],
                "exit_image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}Confirm.png",
                "cooldown": 2
            },
            "ChooseTwo": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}ChooseTwo.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Buff.png", "name": "选择两个buff",
                     "delay": 1},
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Buff.png", "name": "选择两个buff",
                     "delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}ConfirmTwo.png",
                "cooldown": 2
            },
            "ChooseCard": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Card.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Card.png", "name": "选择card", "delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Confirm.png",
                "cooldown": 2  # 模式执行后的冷却时间
            },
            "ChooseOne": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}ChooseOne.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Buff.png", "name": "选择一个buff", "delay": 1},
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Buff.png","name": "选择一个buff", "delay": 1},
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Gear.png", "name": "选择一个战备","delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Confirm.png",
                "cooldown": 2
            },
            "Confirm": {
                "entry_image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}Confirm0.png",
                "actions": [
                    {
                        "image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}Confirm0.png",
                        "name": "确认",
                        "delay": 1},
                ],
                "exit_image": "skip",
                "cooldown": 2  # 模式执行后的冷却时间
            },
            "ChoosePath": {
                "entry_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Path.png",
                "actions": [
                    {"image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}Path.png", "name": "选择路线",
                     "delay": 1},
                ],
                "exit_image": self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}ExitStart.png",
                "cooldown": 2  # 模式执行后的冷却时间
            },
            "Next": {
                "entry_image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}Next.png",
                "actions": [
                    {"image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}Next.png","name": "选择路线","delay": 1},
                ],
                "exit_image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}NextConfirm0.png",
                "cooldown": 2  # 模式执行后的冷却时间
            },
            "TheEnd": {
                "entry_image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}TheEnd.png",
                "actions": [
                    {
                        "image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}TheEnd.png",
                        "name": "选择路线", "delay": 1},
                ],
                "exit_image": self.rec.source_path + "Game-Assistant\\Source\\" + f"{self.rec.resolutionRatio[0]}Finish.png",
                "cooldown": 2  # 模式执行后的冷却时间
            },
        }
        # 验证所有图片文件是否存在
        # self._validate_image_files()
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
        """执行指定模式的动作序列（带容错机制）"""
        print(f"[模式激活] {self.current_mode}")
        click_history = {}  # 存储已点击过的位置 {图片路径: [坐标列表]}
        success_count = 0  # 记录成功执行的动作数

        for action in mode_config["actions"]:
            if action.get("skip", False):
                continue
            print(f"正在执行: {action['name']}")
            action_done = False
            attempts = 0
            max_attempts = action.get("max_attempts", 3)  # 最大尝试次数，默认为3
            # 带超时检测的执行循环
            while self.running and attempts < max_attempts:
                found = self.rec.ToRecognizeWhere(action["image"])
                if found:
                    current_pos = (self.rec.x, self.rec.y)
                    if action.get("is_skip", False):
                        action["skip"] = True

                    # 重复点击检查
                    if self._is_duplicate_click(action["image"], current_pos, click_history):
                        print(f"检测到重复位置: {current_pos}，尝试向右偏移600像素")
                        offset_pos = (current_pos[0] + convert_coordinates(600,0,(2560,1440),self.rec.resolutionRatio)[0], current_pos[1])  # 向右偏移600像素

                        # 确保偏移后的位置在屏幕范围内
                        screen_width, screen_height = pyautogui.size()
                        if offset_pos[0] > screen_width:
                            offset_pos = (screen_width - convert_coordinates(100,0,(2560,1440),self.rec.resolutionRatio)[0], offset_pos[1])  # 如果超出屏幕右侧，调整到屏幕边缘
                            print(f"调整偏移位置到屏幕边缘: {offset_pos}")

                        print(f"执行 {action['name']} (偏移位置: {offset_pos})")
                        pyautogui.click(*offset_pos)
                        time.sleep(action["delay"])

                        # 记录原始点击位置（不是偏移后的位置）
                        self._record_click(action["image"], current_pos, click_history)
                        action_done = True
                        success_count += 1
                        break

                    # 执行点击操作（非重复位置）
                    print(f"执行 {action['name']} ({current_pos})")
                    pyautogui.click(*current_pos)
                    time.sleep(action["delay"])

                    # 记录点击历史
                    self._record_click(action["image"], current_pos, click_history)
                    action_done = True
                    success_count += 1
                    break

                attempts += 1

            if not action_done:
                print(f"跳过未找到的: {action['name']}")

        # 退出确认处理（无论是否成功执行动作）
        print("处理退出确认...")
        exit_found = False
        exit_start = time.time()
        while self.running and time.time() - exit_start < 3:
            # if mode_config["exit_image"]==self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}ExitStart.png" or mode_config["exit_image"]== self.rec.source_path+"Game-Assistant\\Source\\"+f"{self.rec.resolutionRatio[0]}ExitLottery.png":
            #     keyboard = pynput.keyboard.Controller()
            #     keyboard.press(pynput.keyboard.Key.esc)
            #     time.sleep(0.5)
            #     keyboard.release(pynput.keyboard.Key.esc)
            #     exit_found = True
            #     break
            if mode_config["exit_image"] =="skip" or self.rec.ToRecognizeWhere(mode_config["exit_image"]):
                pyautogui.click(self.rec.x, self.rec.y)
                exit_found = True
                break
        if self.current_mode == "TheEnd" and exit_found:
            self.the_end_complete += 1
            if self.the_end_complete>self.limit:
                #结束
                pass
            else:
                original_res = (2560, 1440)
                target_res = pyautogui.size()
                size_t = 0
                if target_res[0] / target_res[1] != 16 / 9:
                    size_t = (target_res[1] - target_res[0] / 16 * 9) / 2
                sleep(3)
                pyautogui.click(convert_coordinates(1750, 789 - size_t, original_res, target_res))  # (x,y)战线肃清
                sleep(1)
                pyautogui.click(convert_coordinates(1750, 789 - size_t, original_res, target_res))  # (x,y)点一个buff
                sleep(1)
                pyautogui.click(convert_coordinates(2274, 1372 - size_t, original_res, target_res))  # (x,y)下一步
                sleep(1)
                pyautogui.click(convert_coordinates(2274, 1372 - size_t, original_res, target_res))  # (x,y)出战



        return success_count > 0 or exit_found

    def _is_duplicate_click(self, image_path, current_pos, history):
        """重复点击检测"""
        if image_path not in history:
            return False

        # 考虑屏幕缩放因素
        screen_scale = 1.0  # 可通过OCR获取实际屏幕缩放比例
        threshold = 15 * screen_scale

        # 计算最小曼哈顿距离（性能更优）
        min_distance = min(
            abs(current_pos[0] - x) + abs(current_pos[1] - y)
            for (x, y) in history[image_path]
        )

        return min_distance < threshold

    def _record_click(self, image_path, position, history):
        """记录点击位置"""
        if image_path not in history:
            history[image_path] = []
        history[image_path].append(position)

    def _get_search_regions(self, screen_w, screen_h, margin=50, exclude=[]):
        """生成智能搜索区域（避开已点击位置）"""
        # 基础分区：将屏幕划分为3x3网格
        regions = []
        cell_w = (screen_w - 2 * margin) // 3
        cell_h = (screen_h - 2 * margin) // 3

        for i in range(3):
            for j in range(3):
                left = margin + i * cell_w
                top = margin + j * cell_h
                regions.append((left, top, cell_w, cell_h))

        # 排除已点击区域周围的区块
        filtered_regions = []
        for (x, y) in exclude:
            for region in regions:
                r_left, r_top, r_w, r_h = region
                if not (r_left < x < r_left + r_w and r_top < y < r_top + r_h):
                    filtered_regions.append(region)

        return filtered_regions if filtered_regions else regions
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

                if self.rec.ToRecognizeWhere(config["entry_image"]):
                    self.current_mode = mode_name
                    print("buff设置为True")
                    self.lock[0] += 1
                    self.lock[1] += 1
                    print(f"Buff:防卡上锁{self.lock[0]},Buff\n空房间环视一周上锁{self.lock[1]}")
                    self.buff=True
                    if self._execute_mode_actions(config):
                        last_mode_time = time.time()
                    print("buff设置为False")
                    self.lock[0] -= 1
                    self.lock[1] -= 1
                    print(f"Buff:防卡解锁{self.lock[0]},Buff\n空房间环视一周解锁{self.lock[1]}")
                    self.buff = False
                    break
            self.va()
            time.sleep(0.2)

    def start(self):
        """启动检测线程"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._mode_detection_loop, daemon=True)
            self.thread.start()
            # print("buff-------------------------已启动")

    def stop(self):
        """停止检测"""
        if self.running:
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join()
            print("已停止")
    def pa(self):
        self.sa-=1
        while self.sa<0:
            time.sleep(1)

    def va(self):
        if self.sa<0:
            self.sa+=1

def BUFF():
    selector = BuffSelector()
    selector.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        selector.stop()
        print("程序已安全退出")



if __name__ == "__main__":
    print("3秒后开始运行...")
    sleep(3)  # 初始等待时间
    BUFF()
