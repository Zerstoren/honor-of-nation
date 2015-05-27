import tests.backend.t_controller.generic

from tests.package.db.town import Town
from tests.package.db.equipment import Equipment
from tests.package.db.army import Army

from models.UserState import Common as CommonUserState

import service.User
import service.Army

import controller.BattleController


class _Abstract_Controller(
    tests.backend.t_controller.generic.Backend_Controller_Generic,
    Town,
    Equipment,
    Army
):

    def _getMainBattleController(self):
        return controller.BattleController.MainController()


class Backend_Controller_BattleCeleryTest(_Abstract_Controller):
    def setUp(self):
        self.initCelery(debug=True)
        super().setUp()
        self.transfer = self._login()
        self.user = self.transfer.getUser()
        self.terrain = self.fillTerrain(0, 0, 2, 2)
        self.town = self.addTown(0, 0, self.user, 1)

        self.armor = self.createEquipmentArmor(self.user, health=0, agility=0, absorption=0)
        self.weapon = self.createEquipmentWeapon(self.user, damage=0, speed=0, critical_chance=0, critical_damage=0)
        self.unit = self.createEquipmentUnit(
            self.user,
            health=0,
            agility=0,
            absorption=0,
            stamina=0,
            strength=0,
            armor=self.armor,
            weapon=self.weapon
        )

        self.unitGeneral = self.createEquipmentUnit(
            self.user,
            uType='general',
            troopSize=50000,
            health=0,
            agility=0,
            absorption=0,
            stamina=0,
            strength=0,
            armor=self.armor,
            weapon=self.weapon
        )

    def testAttack(self):
        self.unitGeneral = self.createEquipmentUnit(
            self.user,
            uType='general',
            troopSize=50000,
            health=0,
            agility=0,
            absorption=0,
            stamina=0,
            strength=0,
            armor=self.armor,
            weapon=self.weapon
        )

        serviceArmy = service.Army.Service_Army()

        self.user1 = self.fixture.getUser(2)
        self.town1 = self.addTown(0, 1, self.user1, 1)

        solider = self.createArmy(self.town, self.unit, count=1000)
        general = self.createArmy(self.town, self.unitGeneral, count=1000)
        self.setArmySoliderToGeneral(solider, general)

        solider1 = self.createArmy(self.town1, self.unit, count=1000)
        general1 = self.createArmy(self.town1, self.unitGeneral, count=1000)
        self.setArmySoliderToGeneral(solider1, general1)

        serviceArmy.moveOutBuild(general)
        serviceArmy.moveOutBuild(general1)

        service.User.Service_User().getUserState(self.user, self.user1)
        service.User.Service_User().setUserState(self.user, self.user1, CommonUserState.STATE_WAR)

        self.fastMove(general1, 0, 0)

        msg = self.transfer.getLastMessage()

        self._getMainBattleController().acceptBattle(
            self.transfer,
            {
                'mapPosition': 0,
                'user': str(self.user.getId()),
                'accept': True,
                'units': {
                    msg['message']['army'][0]['_id']: True
                }
            }
        )

        import time
        time.sleep(4)
