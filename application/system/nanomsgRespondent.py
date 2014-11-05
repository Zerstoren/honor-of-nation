import config
import nanomsg

import pickle

import threading


class Respondent_Instance():
    def __init__(self):
        self.messanger = nanomsg.Socket(protocol=nanomsg.RESPONDENT)
        self.messanger.connect(config.get('nanomsg.everybody.respondent'))

    def onMessage(self, data):
        result, userId = self._onMessage(data['data'], data['user'])

        self.messanger.send(pickle.dumps({
            'connect': data['connect'],
            'user': userId,
            'data': result
        }))

    def setHandler(self, handler):
        self._onMessage = handler

    def run(self):
        while True:
            info = self.messanger.recv()

            self.onMessage(pickle.loads(info))
            # thread = threading.Thread(
            #     target=self.onMessage,
            #     args=(pickle.loads(info),)
            # )

            # thread.start()

Respondent = Respondent_Instance()