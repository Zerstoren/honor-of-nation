from network.battle_server.receiver import Receiver
from battle.prepare import Prepare


class IncomingBattle_Instance(object):
    def __init__(self):
        Receiver.setOnMessage(self.onMessage)

    def onMessage(self, msg):
        defenders = msg['defenders']
        attackers = msg['attackers']

        prepare = Prepare(defenders, attackers)





IncomingBattle = IncomingBattle_Instance()
