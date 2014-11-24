import config
import time
import json

import system.log


class MainController():
    def get(self, transfer, data):
        transfer.send('/system/configs', {
            'done': True,
            'data': {
                'time': int(time.time()),

                'admin_mode': config.get('game.admin_mode') == "true",

                'rate_build_up': int(config.get('rate.build_up')),
                'rate_base_rate': int(config.get('rate.base_rate')),

                'map_size': int(config.get('map.size')),
                'chunk_size': int(config.get('map.chunk'))
            }
        })

    def error(self, transfer, data):
        system.log.error("JS ERROR: " + str(data['error']) + "\n\n" + str(data['file']) + "\n\n" + str(data['stack']))

    def log(self, transfer, data):
        system.log.warn("JS LOG: " + json.dumps(data))
