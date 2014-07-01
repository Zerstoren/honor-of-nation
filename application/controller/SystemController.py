import config
import time


class MainController():
    def get(self, transfer, data):
        transfer.send('/system/configs', {
            'time': int(time.time()),

            'admin_mode': config.get('game.admin_mode') == "true",

            'map_size': int(config.get('map.size')),
            'chank_size': int(config.get('map.chank'))
        })
