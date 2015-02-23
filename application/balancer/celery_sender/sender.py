import config
import system.connect.client
import system.log

import json
import pickle
import zlib


class Respondent_Instance(system.connect.client.TCPWrapper):
    def writeMessage(self, data, user):
        try:
            sendData = pickle.dumps({
                'socketId': None,
                'user': user,
                'data': zlib.compress(
                    bytes(
                        json.dumps(data),
                        'utf-8'
                    ),
                    5
                )
            })
        except Exception as e:
            import traceback
            system.log.critical(e)
            system.log.critical(traceback.format_exc())
            return

        self.write(sendData)

Respondent = Respondent_Instance(
    config.get('balancer.celery.client.host'),
    int(config.get('balancer.celery.client.port'))
)
