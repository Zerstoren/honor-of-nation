import tests.backend.t_controller.generic

from tests.package.db.town import Town
from tests.package.db.equipment import Equipment
from tests.package.db.army import Army

import controller.ArmyQueueController
import controller.ArmyController

import service.ArmyQueue
import service.Army

import time

import tests.rerun

import exceptions.database


class _Abstract_Controller(
    tests.backend.t_controller.generic.Backend_Controller_Generic,
    Town,
    Equipment,
    Army
):

    def _getArmyController(self):
        return controller.ArmyController.MainController()

    def _getArmyQueueController(self):
        return controller.ArmyQueueController.MainController()

    def _getArmyQueueCollectionController(self):
        return controller.ArmyQueueController.CollectionController()

    def _getArmyService(self):
        return service.Army.Service_Army()

    def _getArmyQueueService(self):
        return service.ArmyQueue.Service_ArmyQueue()


class Backend_Controller_ArmyTest(_Abstract_Controller):
    def setUp(self):
        super().setUp()
        self.transfer = self._login()
        self.terrain = self.fillTerrain(0, 0, 1, 1)
        self.user = self.transfer.getUser()
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

    def testServiceCreateArmy(self):
        armyService = service.Army.Service_Army()
        armyDomain = armyService.create(
            self.unit,
            self.town,
            100
        )

        testData = armyDomain._domain_data
        del testData['_id']

        self.assertEqual(
            testData,
            {
                'unit': self.unit.getId(),
                'user': self.user.getId(),
                'location': 0,
                'commander': None,
                'count': 100,
                'formation': None,
                'in_build': True,
                'is_general': False,
                'mode': 1,
                'move_path': {},
                'power': 100,
                'suite': None
            }
        )

    def testLoadArmy(self):
        town2 = self.addTown(0, 1, self.user, 1)

        self.createArmy(self.town, self.unit, 100)
        self.createArmy(self.town, self.unit, 100)
        self.createArmy(town2, self.unit, 120)

        armyController = controller.ArmyController.CollectionController()
        armyController.load(
            self.transfer,
            {
                'user': str(self.user.getId()),
                'pos_id': str(self.town.getMap().getPosition().getPosId())
            }
        )

        result = self.transfer.getLastMessage()['message']
        self.assertTrue(result['done'])
        self.assertEqual(2, len(result['data']))

    def testRemoveArmyFromQueue(self):
        armyController = self._getArmyQueueController()
        resourceDomain = self.user.getResources()
        armyController.create(
            self.transfer,
            {
                'town': str(self.town.getId()),
                'unit': str(self.unit.getId()),
                'count': 50
            }
        )
        firstFixResources = resourceDomain.toDict()

        armyController.create(
            self.transfer,
            {
                'town': str(self.town.getId()),
                'unit': str(self.unit.getId()),
                'count': 25
            }
        )
        queueDomain1, queueDomain2 = self._getArmyQueueService().getQueue(self.town)

        armyController.remove(
            self.transfer,
            {
                'town': str(self.town.getId()),
                'queue_id': str(queueDomain1.getId())
            }
        )
        thirdFixResources = resourceDomain.toDict()

        queue = self._getArmyQueueService().getQueue(self.town)
        self.assertEqual(
            len(queue),
            1
        )
        self.assertEqual(
            queue[0].getCount(),
            25
        )
        self.assertDictEqual(firstFixResources, thirdFixResources)

    def testGetQueue(self):
        self.createArmyQueue(self.town, self.unit, count=10)
        self.createArmyQueue(self.town, self.unit, count=25)

        armyController = self._getArmyQueueCollectionController()
        armyController.load(
            self.transfer,
            {
                'town': str(self.town.getId())
            }
        )

        result = self.transfer.getLastMessage()['message']['data']

        self.assertEqual(len(result), 2)

        self.assertEqual(result[0]['count'], 10)
        self.assertEqual(result[1]['count'], 25)


class Backend_Controller_ArmyCeleryTest(_Abstract_Controller):
    def setUp(self):
        self.initCelery(True)
        super().setUp()
        self.transfer = self._login()
        self.terrain = self.fillTerrain(0, 0, 2, 2)
        self.user = self.transfer.getUser()
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

    @tests.rerun.retry(retry=10)
    def testRemoveArmyFromQueuePartial(self):
        self._getArmyQueueController().create(
            self.transfer,
            {
                'town': str(self.town.getId()),
                'unit': str(self.unit.getId()),
                'count': 5
            }
        )

        time.sleep(1)

        queueDomain = self._getArmyQueueService().getQueue(self.town)[0]
        self._getArmyQueueController().remove(
            self.transfer,
            {
                'town': str(self.town.getId()),
                'queue_id': str(queueDomain.getId())
            }
        )

        armyDomain = service.Army.Service_Army().load(
            self.user,
            self.town.getMap().getPosition()
        )[0]

        self.assertEqual(armyDomain.getCount(), 1)

    @tests.rerun.retry()
    def testCreateArmy(self):
        armyController = self._getArmyQueueController()
        armyController.create(
            self.transfer,
            {
                'town': str(self.town.getId()),
                'unit': str(self.unit.getId()),
                'count': 1
            }
        )

        queue = service.ArmyQueue.Service_ArmyQueue().getQueue(self.town)

        time.sleep(3)

        townUnits = self._getArmyService().load(self.user, self.town.getMap().getPosition())
        result = townUnits[0].toDict()
        del result['_id']

        self.assertTrue(self.transfer.getLastMessage()['message']['done'])
        self.assertEqual(len(queue), 1)
        self.assertTrue(bool(queue[0].getQueueCode()))
        self.assertDictEqual(
            result,
            {
                'user': self.user.getId(),
                'unit': self.unit.getId(),
                'location': self.town.getMap().getPosition().getPosId(),
                'count': 1,
                'commander': None,
                'formation': None,
                'in_build': True,
                'mode': 1,
                'is_general': False,
                'move_path': {},
                'power': 100,
                'suite': None
            }
        )

    @tests.rerun.retry()
    def testMove(self):
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

        solider = self.createArmy(self.town, self.unit, count=100)
        general = self.createArmy(self.town, self.unitGeneral, count=100)
        self.setArmySoliderToGeneral(solider, general)
        self.setArmyLeaveTown(general)

        self._getArmyController().move(
            self.transfer,
            {
                'army_id': str(general.getId()),
                'path': [[1,1], [2,2]]
            }
        )


        self.assertEqual(general.getLocation(), 0)
        time.sleep(6)
        general.extract(True)
        self.assertEqual(general.getLocation(), 2001)


class Backend_Controller_Army_ManipulationTest(_Abstract_Controller):
    def setUp(self):
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

    def testLoadDetails(self):
        commander = self.createArmy(self.town, self.unitGeneral)
        commanderSuite = self.createArmy(self.town, self.unit)
        general1 = self.createArmy(self.town, self.unitGeneral)
        suiteGeneral1 = self.createArmy(self.town, self.unit)
        soliders1General1 = self.createArmy(self.town, self.unit)
        soliders2General1 = self.createArmy(self.town, self.unit)
        general2 = self.createArmy(self.town, self.unitGeneral)
        suiteGeneral2 = self.createArmy(self.town, self.unit)
        soliders1General2 = self.createArmy(self.town, self.unit)
        soliders2General2 = self.createArmy(self.town, self.unit)

        armyService = self._getArmyService()
        armyService.addSuite(commander, commanderSuite)
        armyService.addSuite(general1, suiteGeneral1)
        armyService.addSuite(general2, suiteGeneral2)

        armyService.addSolidersToGeneral(general1, [soliders1General1, soliders2General1])
        armyService.addSolidersToGeneral(general2, [soliders1General2, soliders2General2])
        armyService.addSolidersToGeneral(commander, [general1, general2])

        self._getArmyController().detail(self.transfer, {
            'user': str(self.user.getId()),
            'army': str(commander.getId())
        })

        result = self.transfer.getLastMessage()['message']

        self.assertEqual(result['current']['_id'], str(commander.getId()))
        self.assertEqual(result['suite']['_id'], str(commanderSuite.getId()))

        self.assertEqual(2, len(result['sub_army']))

        dictGeneral1 = result['sub_army'][0]
        self.assertEqual(dictGeneral1['current']['_id'], str(general1.getId()))
        self.assertEqual(dictGeneral1['suite']['_id'], str(suiteGeneral1.getId()))
        self.assertEqual(dictGeneral1['sub_army'][0]['current']['_id'], str(soliders1General1.getId()))
        self.assertEqual(dictGeneral1['sub_army'][1]['current']['_id'], str(soliders2General1.getId()))

        dictGeneral2 = result['sub_army'][1]
        self.assertEqual(dictGeneral2['current']['_id'], str(general2.getId()))
        self.assertEqual(dictGeneral2['suite']['_id'], str(suiteGeneral2.getId()))
        self.assertEqual(dictGeneral2['sub_army'][0]['current']['_id'], str(soliders1General2.getId()))
        self.assertEqual(dictGeneral2['sub_army'][1]['current']['_id'], str(soliders2General2.getId()))

    def testMoveInBuild(self):
        army = self.createArmy(self.town, self.unitGeneral)
        army.setInBuild(False)
        army.getMapper().save(army)

        self._getArmyController().moveInBuild(
            self.transfer,
            {
                'army': str(army.getId())
            }
        )

        army.extract(force=True)
        self.assertTrue(army.getInBuild())

    def testMoveOutBuild(self):
        army = self.createArmy(self.town, self.unitGeneral)

        self._getArmyController().moveOutBuild(
            self.transfer,
            {
                'army': str(army.getId())
            }
        )

        army.extract(force=True)
        self.assertFalse(army.getInBuild())

    def testMerge(self):
        army = self.createArmy(self.town, self.unit, count=25)
        army2 = self.createArmy(self.town, self.unit, count=50)

        self._getArmyController().merge(
            self.transfer,
            {
                'army_list': [
                    str(army.getId()),
                    str(army2.getId())
                ]
            }
        )

        try:
            army2.extract(force=True)
            self.fail("Second unit not deleted")
        except exceptions.database.Database:
            pass

        army.extract(force=True)
        self.assertEqual(army.getCount(), 75)

    def testSplit(self):
        army = self.createArmy(self.town, self.unit, count=100)

        self._getArmyController().split(
            self.transfer,
            {
                'army': str(army.getId()),
                'size': '50'
            }
        )

        armyCollection = service.Army.Service_Army().load(
            self.user,
            self.town.getMap().getPosition()
        )


        for domain in armyCollection:
            self.assertEqual(domain.getCount(), 50)

    def testAddSolidersToGeneral(self):
        army = self.createArmy(self.town, self.unit, count=100)
        army2 = self.createArmy(self.town, self.unit, count=200)
        general = self.createArmy(self.town, self.unitGeneral)

        self._getArmyController().addSolidersToGeneral(
            self.transfer,
            {
                'general': str(general.getId()),
                'soliders': [
                    str(army.getId()),
                    str(army2.getId())
                ]
            }
        )

        army.extract(force=True)
        army2.extract(force=True)

        self.assertEqual(
            army.getCommander().getId(),
            general.getId()
        )
        self.assertEqual(
            army2.getCommander().getId(),
            general.getId()
        )

    def testAddGeneralToCommander(self):
        general = self.createArmy(self.town, self.unitGeneral)
        commander = self.createArmy(self.town, self.unitGeneral)

        self._getArmyController().addSolidersToGeneral(
            self.transfer,
            {
                'general': str(commander.getId()),
                'soliders': [
                    str(general.getId())
                ]
            }
        )

        general.extract(force=True)
        self.assertEqual(
            general.getCommander().getId(),
            commander.getId()
        )

    def testRemoveSolidersToGeneral(self):
        army = self.createArmy(self.town, self.unit, count=100)
        army2 = self.createArmy(self.town, self.unit, count=200)
        general = self.createArmy(self.town, self.unitGeneral)

        army.setCommander(general.getId())
        army.getMapper().save(army)
        army2.setCommander(general.getId())
        army2.getMapper().save(army2)

        self._getArmyController().removeSolidersGeneral(
            self.transfer,
            {
                'general': str(general.getId()),
                'soliders': [
                    str(army.getId()),
                    str(army2.getId())
                ]
            }
        )

        army.extract(force=True)
        army2.extract(force=True)

        self.assertEqual(
            army.getCommander(),
            None
        )
        self.assertEqual(
            army2.getCommander(),
            None
        )

    def testAddSuite(self):
        army = self.createArmy(self.town, self.unit, count=100)
        general = self.createArmy(self.town, self.unitGeneral)

        self._getArmyController().addSuite(
            self.transfer,
            {
                'general': str(general.getId()),
                'solider': str(army.getId())
            }
        )

        army.extract(force=True)
        general.extract(force=True)

        self.assertEqual(army.getCommander().getId(), general.getId())
        self.assertEqual(general.getSuite().getId(), army.getId())

    def testRemoveSuite(self):
        army = self.createArmy(self.town, self.unit, count=100)
        general = self.createArmy(self.town, self.unitGeneral)

        army.setCommander(general.getId())
        army.getMapper().save(army)

        general.setSuite(army.getId())
        general.getMapper().save(general)

        self._getArmyController().removeSuite(
            self.transfer,
            {
                'general': str(general.getId()),
                'solider': str(army.getId())
            }
        )

        army.extract(force=True)
        general.extract(force=True)

        self.assertEqual(army.getCommander(), None)
        self.assertEqual(general.getSuite(), None)

    def testDissolution(self):
        army = self.createArmy(self.town, self.unit, count=100)

        self._getArmyController().dissolution(
            self.transfer,
            {
                'army': str(army.getId())
            }
        )

        try:
            army.extract(force=True)
            self.fail("Army not deleted")
        except exceptions.database.Database:
            pass

    def testMove(self):
        solider = self.createArmy(self.town, self.unit, count=100)
        general = self.createArmy(self.town, self.unitGeneral, count=100)
        self.setArmySoliderToGeneral(solider, general)
        self.setArmyLeaveTown(general)

        self._getArmyController().move(
            self.transfer,
            {
                'army_id': str(general.getId()),
                'path': [[1,1], [2,2]]
            }
        )

        general.extract(True)
        testedDict = general.getMovePath()
        del testedDict['code']
        del testedDict['start_at']
        self.assertDictEqual(
            testedDict,
            {
                'pos_id': 2001,
                'complete_after': 5,
                'power': 8
            }
        )
