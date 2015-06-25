from tests.generic import Generic
from tests.package.db.army import Army
from tests.package.db.town import Town
from tests.package.db.equipment import Equipment

from battle.prepare import Prepare


class Battle_Generic(
    Generic,
    Army,
    Town,
    Equipment
):
    def setUp(self):
        super().setUp()
        self.attackerUser = self.fixture.getUser(0)
        self.defenderUser = self.fixture.getUser(1)
        self.fillTerrain(0, 0, 1, 1)

        self.townAttacker = self.addTown(0, 0, self.attackerUser)
        self.townDefender = self.addTown(1, 0, self.defenderUser)

    def prepare(self, attackers, defenders):
        attacker = []
        defender = []

        for i in attackers:
            attacker.append(
                str(str(i.getId()))
            )

        for i in defenders:
            defender.append(
                str(str(i.getId()))
            )

        Prepare(defender, attacker)
