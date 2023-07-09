from Functions.game_functions import press_key_multiple, get_text_from_color, press_key, move_mouse
from Functions.game_data import PortDataParser
from PIL import ImageGrab
import pytesseract
import time
import asyncio
import numpy as np
import config

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 创建一个图片的列表
prepareImages = [
    'Images/start.png',
    'Images/ok.png',
    'Images/playBattle.png',
    'Images/loading.png',
    'Images/gameReady.png',
]

#准备加入游戏
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
            target, data = await asyncio.gather(
                parser.get_map_obj_data(["enemyAir", "me"]),
                parser.get_state_data(["THR", "IAS", "SPD", "ALT"])
            )
            print(target)
            print(data)

            # 如果是第一次接收到ALT数据，就将其存储起来
            if initial_ALT is None and "ALT" in data:
                initial_ALT = data["ALT"]
                print(f"Initial ALT: {initial_ALT}")

            # 如果节流阀值低于最大节流阀值，就按住左Shift键
            if "THR" in data and data["THR"] < config.max_throttle:
                press_key('shift_l', config.data_waiting_time)

            # 如果速度大于起飞速度，就开始按下S键，并持续按下直到飞机达到设定的飞行高度
            if "SPD" in data and data["SPD"] > config.takeoff_speed:
                while True:
                    data = await parser.get_state_data(["ALT"])
                    if "ALT" in data and data["ALT"] - initial_ALT > config.flight_altitude:
                        break
                    press_key('s', config.data_waiting_time)
                    time.sleep(config.data_waiting_time)

            time.sleep(config.data_waiting_time)

    finally:
        await parser.close()

asyncio.run(main())