import config
import system.connect.client

import pickle
import system.log


class Respondent_Instance(system.connect.client.TCPWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setReadListener(self.onMessage)

    def processMessage(self, data):
        data = pickle.loads(data)
        result, userId = self._onMessage(data['data'], data['user'])

        return {
            'connect': data['connect'],
            'user': userId,
            'data': result
        }

    def onMessage(self, connect, data):
        try:
            result = self.processMessage(data)

            if config.isDevelopment():
                import json
                json.dumps(result)

        except Exception as e:
            import traceback
            system.log.critical(e)
            system.log.critical(traceback.format_exc())
            return

        self.write(
            pickle.dumps(
                result
            )
        )

    def setHandler(self, handler):
        self._onMessage = handler


Respondent = Respondent_Instance(
    config.get('balancer.backend.client.host'),
    int(config.get('balancer.backend.client.port'))
)
