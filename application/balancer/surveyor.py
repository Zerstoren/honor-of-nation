import config
import system.connect.server

import pickle
import json

import balancer.clientConnector

class Surveyor_Instance(system.connect.server.BalancerBroker):
    def send(self, userConnector, data):
        request = {
            'connect': userConnector.getSocketId(),
            'user': userConnector.getUser(),
            'data': data
        }

        self.write(pickle.dumps(request))

    def onMessage(self, connector, data):
        toSend, socketId, userConnector = self._processData(data)

        userConnector.send(
            json.dumps(toSend)
        )

    def _processData(self, data):
        info = pickle.loads(data)

        userConnector = balancer.clientConnector.ClientPool.get(info['connect'])
        userConnector.setUser(info['user'])

        return (info['data'], info['connect'], userConnector, )
    #
    # def stop(self):
    #     self.close()

Surveyor = Surveyor_Instance(
    config.get('balancer.backend.server.host'),
    int(config.get('balancer.backend.server.port'))
)
