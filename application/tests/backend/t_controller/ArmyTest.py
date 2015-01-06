import tests.backend.t_controller.generic

from tests.package.db.town import Town
from tests.package.db.equipment import Equipment
from tests.package.db.army import Army

import controller.ArmyQueueController

import service.ArmyQueue
import service.Army

import time


class Backend_Controller_ArmyTest(
    tests.backend.t_controller.generic.Backend_Controller_Generic,
    Town,
    Equipment,
    Army
):
    def setUp(self):
        self.initCelery()
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

    def _getArmyController(self):
        return

    def _getArmyQueueController(self):
        return controller.ArmyQueueController.MainController()

    def _getArmyQueueCollectionController(self):
        return controller.ArmyQueueController.CollectionController()

    def _getArmyService(self):
        return service.Army.Service_Army()

    def _getArmyQueueService(self):
        return service.ArmyQueue.Service_ArmyQueue()

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
                'count': 100
            }
        )

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

        time.sleep(2)

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
                'commander': None
            }
        )

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
        self.createQueue(self.town, self.unit, count=10)
        self.createQueue(self.town, self.unit, count=25)

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
