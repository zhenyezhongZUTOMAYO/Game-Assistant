from pynput import mouse


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


def on_click(x, y, button, pressed):
    if pressed:
        print(f'鼠标点击坐标: ({x}, {y})，按钮: {button}')


if __name__ =="__main__":
    # 创建鼠标监听器
    listener = mouse.Listener(on_click=on_click)

    print("开始监听鼠标点击，按ESC键停止...")

    # 启动监听器
    listener.start()

    # 保持程序运行
    try:
        while listener.is_alive():
            pass
    except KeyboardInterrupt:
        pass
    finally:
        # 停止监听器
        listener.stop()
        print("\n鼠标监听已停止")
    # print(convert_coordinates(1980, 1963,(3840,2160),(2560,1440)))
    # print(convert_coordinates(3415, 1747,(3840,2160),(2560,1440)))
    # print(convert_coordinates(2070, 1355,(3840,2160),(2560,1440)))
