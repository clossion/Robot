import aiohttp
import asyncio
from .game_message import state_key_dict, map_obj_key_dict

class PortDataParser:
    ports = {
        "HUD": "http://localhost:8111/hudmsg",
        "CHAT": "http://localhost:8111/gamechat",
        "INDICATORS": "http://localhost:8111/indicators",
        "MAP_OBJ": "http://localhost:8111/map_obj.json",
        "MAP_INFO": "http://localhost:8111/map_info.json",
        "MISSION": "http://localhost:8111/mission.json",
        "STATE": "http://localhost:8111/state",
        "MAP_IMG": "http://localhost:8111/map.img",
        # 添加其他端口
    }

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def parse_state_data(self, data, keys):
        result = {}
        for key in keys:
            full_key = state_key_dict.get(key)
            if full_key:
                result[key] = data.get(full_key)
        return result

    async def parse_map_obj_data(self, data, keys):
        result = {}
        for item in data:
            obj_icon = item.get("icon")
            if obj_icon and obj_icon in keys:
                result[obj_icon] = item
        return result

    async def get_state_data(self, keys):
        url = self.ports.get("STATE")
        if url:
            async with self.session.get(url) as response:
                data = await response.json()
                if isinstance(data, dict):
                    parsed_data = await self.parse_state_data(data, keys)
                    return parsed_data
                else:
                    return data
        else:
            return "Invalid port name or no key dictionary for this port"

    async def get_map_obj_data(self, keys):
        url = self.ports.get("MAP_OBJ")
        if url:
            async with self.session.get(url) as response:
                data = await response.json()
                if isinstance(data, list):
                    keys = [map_obj_key_dict.get(key) for key in keys]
                    return await self.parse_map_obj_data(data, keys)
                else:
                    return data
        else:
            return "Invalid port name or no key dictionary for this port"

    async def close(self):
        await self.session.close()
