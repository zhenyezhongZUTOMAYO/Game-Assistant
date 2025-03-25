import Recognize
import pyautogui
import threading

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


class SpeakNpc:
    def __init__(self):
        self.rec=Recognize.Recognize()
    def isBuff(self):
        if self.rec.ToRecognizeWhere(self.rec.source_path+"Game-Assistant\\Source\\"+str(self.rec.resolutionRatio[0])+"Buff1.png") is not False:
            self.Buff1()
        if self.rec.ToRecognizeIsHave(self.rec.source_path + "Game-Assistant\\Source\\" + str(self.rec.resolutionRatio[0]) + "TestSpeak1.png") is not False:
            self.Speak()
            
    def Buff1(self):
        # buff1
        """(1320, 1308)
        (2276, 1164)
        (1380, 903)
        """
        pyautogui.click(convert_coordinates(1320, 1308, (2560, 1440), self.rec.resolutionRatio))
        pyautogui.click(convert_coordinates(2276, 1164, (2560, 1440), self.rec.resolutionRatio))
        pyautogui.click(convert_coordinates(1380, 903, (2560, 1440), self.rec.resolutionRatio))
    def Speak(self):
        """
            这是一个与人对话的函数如果2秒内未出现与人交流的白点那么退出识别
            :return: None
            """
        rec = Recognize.Recognize()
        thread_a = threading.Thread(target=rec.ToRecognizeConWhere, args=[rec.source_path + "Game-Assistant\\Source\\" + str(rec.resolutionRatio[0]) + "TestSpeak1.png", ])
        thread_a.start()
        stop = 0
        while True:
            rec.pa()
            if not thread_a.is_alive():
                return
            if rec.real:
                pyautogui.click(rec.x, rec.y)
                stop = 0
            else:
                """
                识别不到的停止机制如果连续10次识别不到那么终止
                """
                stop += 1
                if stop > 9:
                    rec.end = True
            rec.vb()