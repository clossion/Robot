# Functions/game_functions.py
import json
import pyautogui
import time
import os
import cv2
import pytesseract
import numpy as np
from pynput.keyboard import Controller, Key
from pynput.mouse import Button
from .game_message import image_message_dict, image_action_dict
from PIL import ImageGrab, Image

screen_width, screen_height = pyautogui.size()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 创建一个键盘控制器和鼠标控制器
keyboard = Controller()
mouse = Controller()

def press_key(key, duration=0.1):
    # 如果key是一个字符串，我们需要将其转换为正确的Key对象，或者保持为字符串
    if isinstance(key, str):
        try:
            key = getattr(Key, key)
        except AttributeError:
            pass  # 如果Key对象不存在，那么key就是一个字符串，我们可以直接使用它
    # 按下指定的键
    keyboard.press(key)
    # 等待一段时间，模拟按键持续时间
    time.sleep(duration)
    # 释放指定的键
    keyboard.release(key)
    print(" 执行操作完成")



def move_mouse(location):
    # 移动鼠标到指定的位置
    mouse.position = location
    print(" 执行操作完成")

def click_mouse(location):
    # 移动鼠标到指定的位置并点击
    mouse.position = location
    mouse.click(Button.left)
    print(" 执行操作完成")

def do_nothing():
    # 什么也不做
    pass

def stop_loop():
    # 修改全局变量的值
    global running
    running = False
    print(" 准备战斗中")

# 创建一个操作名称和操作函数的字典
action_function_dict = {
    'press_key': press_key,
    'do_nothing': do_nothing,
    'stop_loop': stop_loop,
}

def press_key_multiple(images):
    # 截取屏幕图片
    screenshot = np.array(ImageGrab.grab())
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    for image_path in images:
        # 读取模板图片
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        template_h, template_w = template.shape[:2]

        # 使用模板匹配找到图片的位置
        res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.9)

        # 如果找到了图片
        if len(loc[0]) > 0:
            # 获取图片的文件名
            image_name = os.path.basename(image_path)
            # 输出已经移动到图片的信息
            print(f" {image_message_dict.get(image_name, image_name)}")
            # 等待1秒
            time.sleep(1)
            # 执行相应的操作
            action_tuple = image_action_dict.get(image_name)
            if action_tuple:
                action_name = action_tuple[0]
                action_args = action_tuple[1:]
                action = action_function_dict.get(action_name)
                if action:
                    action(*action_args)
            # 返回图片的文件名
            return image_name


def get_text_from_color(bbox, lower_color, upper_color):
    # 截取屏幕中的一部分
    img = ImageGrab.grab(bbox=bbox)

    # 将 PIL 图片转换为 OpenCV 图片
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # 创建一个掩码，筛选出特定颜色的像素
    mask = cv2.inRange(img_cv, lower_color, upper_color)

    # 应用掩码
    result = cv2.bitwise_and(img_cv, img_cv, mask=mask)

    # 将 OpenCV 图片转换回 PIL 图片
    img_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

    # 使用 pytesseract 识别图片中的文字
    text = pytesseract.image_to_string(img_pil, config='-c preserve_inter-word_spaces=1')

    return text
