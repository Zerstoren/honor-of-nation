import config
import system.connect.client

import pickle
import json


class Respondent_Instance(system.connect.client.TCPWrapper):
    def writeMessage(self, data, user):
        sendData = pickle.dumps({
            'socketId': None,
            'user': user,
            'data': json.dumps(data)
        })

        self.write(sendData)

Respondent = Respondent_Instance(
    config.get('balancer.celery.client.host'),
    int(config.get('balancer.celery.client.port'))
)
