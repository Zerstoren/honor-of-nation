import config
import system.connect.client

import pickle



class Respondent_Instance(system.connect.client.TCPWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setReadListener(self.onMessage)


    def onMessage(self, connect, data):
        try:
            data = pickle.loads(data)
            result, userId = self._onMessage(data['data'], data['user'])

            self.write(pickle.dumps({
                'connect': data['connect'],
                'user': userId,
                'data': result
            }))
        except Exception as e:
            print(e)

    def setHandler(self, handler):
        self._onMessage = handler


Respondent = Respondent_Instance(
    config.get('balancer.backend.client.host'),
    int(config.get('balancer.backend.client.port'))
)
