from Functions.game_functions import press_key_multiple, get_text_from_color, press_key, move_mouse
from Functions.game_data import PortDataParser
from PIL import ImageGrab
import pytesseract
import time
import asyncio
import numpy as np
import config
import pyautogui
import pydirectinput

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 创建一个图片的列表
prepareImages = [
    'Images/start.png',
    'Images/ok.png',
    'Images/playBattle.png',
    'Images/loading.png',
    'Images/gameReady.png',
]

# 准备加入游戏
# while True:
#     image_name = press_key_multiple(prepareImages)
#     # 如果识别到 'gameReady.png'，就跳出循环
#     if image_name == 'gameReady.png':
#         break
#     # 如果找到了匹配，就等待一段时间，让游戏有时间反应
#     time.sleep(config.wait_time)

# 打破循环后我们就进入了游戏
print('战斗信息指示表')


async def main():
    parser = PortDataParser()

    initial_ALT = None
    try:
        while True:
            target, data, attitude = await asyncio.gather(
                parser.get_map_obj_data(["enemyAir", "me", "point"]),
                parser.get_state_data(["THR", "IAS", "SPD", "ALT"]),
                parser.get_indicators_data(["Pitch", "Pitch1"])
            )
            print(target)

            # 如果是第一次接收到ALT数据，就将其存储起来
            if initial_ALT is None and "ALT" in data:
                initial_ALT = data["ALT"]
                print(f"Initial ALT: {initial_ALT}")

            # 如果节流阀值低于最大节流阀值，就按住左Shift键
            if "THR" in data and data["THR"] < config.max_throttle:
                press_key('shift_l', config.data_waiting_time)

            # 如果SPD大于起飞速度，则向上移动鼠标
            if "ALT" in data and data["ALT"] < config.flight_altitude:
                if "SPD" in data and data["SPD"] > config.takeoff_speed:
                    if attitude["Pitch"] < config.climb_angle:
                        move_mouse(0, -50)  # 向上移动鼠标
                        print("向上移动鼠标")
                    else:
                        move_mouse(0, 50)  # 向下移动鼠标
                        print("向下移动鼠标")
                    time.sleep(config.data_waiting_time)
            else:
                if attitude["Pitch"] < 0:
                    move_mouse(0, -10)  # 向上移动鼠标
                    print("向上移动鼠标")
                else:
                    move_mouse(0, 10)  # 向下移动鼠标
                    print("向下移动鼠标")
            time.sleep(config.data_waiting_time)

    finally:
        await parser.close()


asyncio.run(main())
