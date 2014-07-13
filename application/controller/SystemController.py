import config
import time


class MainController():
    def get(self, transfer, data):
        transfer.send('/system/configs', {
            'done': True,
            'data': {
                'time': int(time.time()),

                'admin_mode': config.get('game.admin_mode') == "true",

                'map_size': int(config.get('map.size')),
                'chunk_size': int(config.get('map.chunk'))
            }
        })
