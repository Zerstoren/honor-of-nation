import config
import time


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
        print(data['error'] + "\n\n" + data['file'] + "\n\n" + data['stack'])
        # raise Exception(data['error'] + "\n\n" + data['file'] + "\n\n" + data['stack'])
