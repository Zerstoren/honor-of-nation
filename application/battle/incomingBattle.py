from network.battle_server.receiver import Receiver
from battle.prepare import Prepare
from battle.simulate.battle import Battle


class IncomingBattle_Instance(object):
    def __init__(self):
        Receiver.setOnMessage(self.onMessage)

    def onMessage(self, msg):
        defenders = msg['defenders']
        attackers = msg['attackers']

        prepare = Prepare(defenders, attackers)
        battle = Battle()
        battle.importData(**prepare.export())
        battle.simulate()

        del prepare
        del battle





IncomingBattle = IncomingBattle_Instance()
