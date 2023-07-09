# Functions/game_message.py

# 创建一个字典，存储图片名称和对应的输出内容
image_message_dict = {
    'start.png': '准备开始游戏',
    'ok.png': '缺少符合要求的载具型号',
    'loading.png': '正在加载中',
    'playBattle.png': '准备加入游戏',
    'gameReady.png': '准备进入战斗',
    # 你可以在这里添加更多的图片和对应的输出内容
}

# 创建一个图片和操作名称的字典
image_action_dict = {
    'start.png': ('press_key', 'enter'),
    'ok.png': ('press_key', 'enter'),
    'playBattle.png': ('press_key', 'enter'),
    'loading.png': ('do_nothing',),
    'gameReady.png': ('do_nothing',),
}

state_key_dict = {
    'THR': 'throttle 1, %',
    'IAS': 'IAS, km/h',
    'SPD': 'TAS, km/h',
    'ALT': 'H, m',
    'Pitch': 'aviahorizon_pitch',
    'Pitch1': 'aviahorizon_pitch1',
    # 添加其他键的缩写
}

map_obj_key_dict = {
    'enemyAir': 'Fighter',
    'me': 'Player',
    'point': 'bombing_point',
    # 添加其他键的缩写
}

