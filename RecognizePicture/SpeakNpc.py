import Recognize
from pyautogui import *

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
        if self.rec.ToRecongnizeIsHave(self.rec.source_path+"Game-Assistant\\Source\\"+str(self.rec.resolutionRatio[0])+"Buff1.png") is not False:
            #buff1
            """(1320, 1308)
            (2276, 1164)
            (1380, 903)
            """
            click(convert_coordinates(1320, 1308,(2560,1440),self.rec.resolutionRatio))
            click(convert_coordinates(2276, 1164,(2560,1440),self.rec.resolutionRatio))
            click(convert_coordinates(1380, 903,(2560,1440),self.rec.resolutionRatio))