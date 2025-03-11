import time

from pynput import keyboard, mouse

def get_mouse_button(key: str) -> mouse.Button:
    real_key = key[6:]  # 取mouse_之后的部分
    return mouse.Button[real_key]

def get_keyboard_button(key: str) :
    if key in keyboard.Key.__members__:
        return keyboard.Key[key]
    elif len(key) == 1:
        return keyboard.KeyCode.from_char(key)
    else:
        return key

def is_mouse_button(key: str) -> bool:
    """
    是否鼠标按键
    :param key:
    :return:
    """
    return key.startswith('mouse_')


def get_button(key: str):
    if is_mouse_button(key):
        return get_mouse_button(key)
    else:
        return get_keyboard_button(key)

class KeyboardMouseController:

    def __init__(self):
        self.keyboard = keyboard.Controller()
        self.mouse = mouse.Controller()

    def tap(self, key: str) -> None:
        """
        按一次按键
        :param key: 按键
        :return:
        """
        if is_mouse_button(key):
            self.mouse.click(get_mouse_button(key))
        else:
            self.keyboard.tap(get_keyboard_button(key))

    def press(self, key: str, press_time= None) -> None:
        """
        :param key: 按键
        :param press_time: 持续按键时间
        :return:
        """
        is_mouse = is_mouse_button(key)
        real_key = get_mouse_button(key) if is_mouse else get_keyboard_button(key)
        if is_mouse:
            self.mouse.press(real_key)
        else:
            self.keyboard.press(real_key)

        if press_time is not None:
            time.sleep(press_time)

            if is_mouse:
                self.mouse.release(real_key)
            else:
                self.keyboard.release(real_key)

    def release(self, key: str) -> None:
        is_mouse = is_mouse_button(key)
        if is_mouse:
            self.mouse.release(get_mouse_button(key))
        else:
            self.keyboard.release(get_keyboard_button(key))
if __name__ == '__main__':
    _c = KeyboardMouseController()
    time.sleep(4)
    t1 = time.time()
    _c.press('c')
    time.sleep(0.5)
    _c.release('c')
    print('%.4f' % (time.time() - t1))

