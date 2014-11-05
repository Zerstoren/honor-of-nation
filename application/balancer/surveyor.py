import config
import nanomsg

import pickle
import json

import threading

import balancer.clientConnector

class Surveyor_Instance():
    def __init__(self):
        self.messanger = nanomsg.Socket(protocol=nanomsg.SURVEYOR)
        self.messanger.bind(config.get('nanomsg.everybody.survey'))
        self.messanger.set_int_option(nanomsg.SURVEYOR, nanomsg.SURVEYOR_DEADLINE, 15000)

    def send(self, connector, data):
        self._send(connector, data)
        # threading.Thread(target=self._send, args=(connector, data)).start()

    def _send(self, connector, data):
        request = {
            'connect': connector.getSocketId(),
            'user': connector.getUser(),
            'data': data
        }

        self.messanger.send(pickle.dumps(request))
        result = self.messanger.recv()

        toSend, socketId = self._processData(connector, result)

        balancer.clientConnector.ClientPool.get(socketId).send(
            json.dumps(toSend)
        )

    def _processData(self, connector, data):
        info = pickle.loads(data)
        connector.setUser(info['user'])
        return (info['data'], info['connect'], )

    def stop(self):
        self.messanger.close()

Surveyor = Surveyor_Instance()
