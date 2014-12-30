from tests.backend.t_controller.equipment.generic import Backend_Controller_Equipment_Generic

import helpers.mongo
import helpers.math

from controller.EquipmentUnitsController import UnitsModelController, UnitsCollectionController
from models.Equipment.Units.Factory import Equipment_Units_Factory

import service.Equipment.Units


class Backend_Controller_Equipment_UnitsTest(Backend_Controller_Equipment_Generic):
    def setUp(self):
        helpers.math.RATE = 100
        super().setUp()

    def tearDown(self):
        helpers.math.RATE = 3
        super().tearDown()

    def init(self):
        super().setUp()
        self.controller = self._getModelController()
        self.transfer = self._login()

    def _getModelController(self):
        return UnitsModelController()

    def _getCollectionController(self):
        return UnitsCollectionController()

    def testGetModel(self):
        self.init()
        uDomain = self.createEquipmentUnit(
            self.transfer.getUser()
        )

        self.controller.get(
            self.transfer,
            {
                '_id': str(uDomain.getId())
            }
        )

        result = self.transfer.getLastMessage()['message']
        self.assertTrue(result['done'])

        del result['data']['armor_data']
        del result['data']['weapon_data']
        del result['weapon_second_data']

        self.assertDictEqual(
            result['data'],
            {
                '_id': str(uDomain.getId()),
                'type': 'solider',
                'user': str(self.transfer.getUser().getId()),
                'armor': str(uDomain.getArmor().getId()),
                'weapon': str(uDomain.getWeapon().getId()),
                'weapon_second': False,
                'absorption': 30,
                'agility': 30,
                'health': 300,
                'stamina': 100,
                'strength': 40,
                'troop_size': 0,
                'time': 482,
                'eat': 138531,
                'rubins': 647926,
                'steel': 145126,
                'wood': 57516
            }
        )

    def testLoadModel(self):
        self.init()
        uDomain1 = self.createEquipmentUnit(
            self.transfer.getUser()
        )
        uDomain2 = self.createEquipmentUnit(
            self.transfer.getUser(),
        )

        uDomain3 = self.createEquipmentUnit(
            self.fixture.getUser(3),
        )

        self._getCollectionController().load(
            self.transfer,
            {
                'user': str(self.transfer.getUser().getId())
            }
        )

        result = self.transfer.getLastMessage()['message']
        self.assertEqual(len(result['data']), 2)

    def testCreateBase(self):
        self.init()
        user = self.transfer.getUser()

        weaponSecond = self.createEquipmentWeapon(user, wType='bow')
        weapon = self.createEquipmentWeapon(user)
        armor = self.createEquipmentArmor(user)

        self.controller.save(self.transfer, {
            'user': str(user.getId()),
            'type': 'general',
            'troop_size': 1000,
            'health': 100,
            'agility': 50,
            'absorption': 50,
            'stamina': 400,
            'strength': 40,
            'armor': str(armor.getId()),
            'weapon': str(weapon.getId()),
            'weapon_second': str(weaponSecond.getId())
        })

        result = self.transfer.getLastMessage()['message']['data']
        unit = Equipment_Units_Factory.get(
            helpers.mongo.objectId(result['_id'])
        )

        self.assertDictEqual(
            unit._domain_data,
            {
                '_id': unit.getId(),
                'user': user.getId(),
                'armor': unit.getArmor().getId(),
                'weapon': unit.getWeapon().getId(),
                'weapon_second': unit.getWeaponSecond().getId(),
                'type': 'general',
                'troop_size': 1000,
                'absorption': 50,
                'agility': 50,
                'health': 100,
                'stamina': 400,
                'strength': 40,
                'eat': 311546,
                'rubins': 1442494,
                'steel': 217161,
                'wood': 221366,
                'time': 960,
                'remove': 0,
            }
        )

    def testCreateBigNumbers(self):
        self.init()

        user = self.transfer.getUser()
        armor = self.createEquipmentArmor(user)
        weapon = self.createEquipmentWeapon(user)

        self.controller.save(self.transfer, {
            'user': str(user.getId()),
            'type': 'general',
            'troop_size': 1000,
            'health': 10000,
            'agility': 500,
            'absorption': 500,
            'stamina': 1200,
            'strength': 4000,
            'armor': str(armor.getId()),
            'weapon': str(weapon.getId()),
            'weapon_second': False
        })

        result = self.transfer.getLastMessage()['message']['data']
        unit = Equipment_Units_Factory.get(
            helpers.mongo.objectId(result['_id'])
        )

        self.assertDictEqual(
            unit._domain_data,
            {
                '_id': unit.getId(),
                'user': user.getId(),
                'armor': armor.getId(),
                'weapon': weapon.getId(),
                'weapon_second': False,
                'type': 'general',
                'troop_size': 1000,
                'absorption': 500,
                'agility': 500,
                'health': 10000,
                'stamina': 1200,
                'strength': 4000,
                'eat': 48987991,
                'rubins': 220190141,
                'steel': 15146653,
                'time': 366598,
                'wood': 22260417,
                'remove': 0
            }
        )

    def testSimulate(self):
        self.init()
        user = self.transfer.getUser()
        weapon = self.createEquipmentWeapon(user)
        armor = self.createEquipmentArmor(user)

        self.controller.save(self.transfer, {
            'user': str(user.getId()),
            'type': 'general',
            'troop_size': 1000,
            'health': 10000,
            'agility': 500,
            'absorption': 500,
            'stamina': 1200,
            'strength': 4000,
            'armor': str(armor.getId()),
            'weapon': str(weapon.getId()),
            'weapon_second': False
        })

        result = self.transfer.getLastMessage()['message']['data']
        unit = Equipment_Units_Factory.get(
            helpers.mongo.objectId(result['_id'])
        )

        self.controller.simulate(self.transfer, {
            'type': 'general',
            'troop_size': 1000,
            'health': 10000,
            'agility': 500,
            'absorption': 500,
            'stamina': 1200,
            'strength': 4000,
            'armor': str(armor.getId()),
            'weapon': str(weapon.getId()),
            'weapon_second': False
        })
        result = self.transfer.getLastMessage()['message']['data']

        del unit._domain_data['user']
        del unit._domain_data['remove']
        del unit._domain_data['_id']
        del result['stamp']
        del result['armor_data']
        del result['weapon_data']
        del result['weapon_second_data']

        unit._domain_data['armor'] = str(unit._domain_data['armor'])
        unit._domain_data['weapon'] = str(unit._domain_data['weapon'])

        self.assertDictEqual(
            unit._domain_data,
            result
        )

    def testChangedValues(self):
        self.init()
        uDomain1 = self.createEquipmentUnit(
            self.transfer.getUser(),
            agility=100
        )
        uDomain2 = self.createEquipmentUnit(
            self.transfer.getUser(),
            agility=200
        )

        self.assertNotEqual(
            uDomain1.getRubins(),
            uDomain2.getRubins()
        )

    def testRemove(self):
        self.init()
        uDomain = self.createEquipmentUnit(
            self.transfer.getUser()
        )
        uDomain2 = self.createEquipmentUnit(
            self.transfer.getUser()
        )

        self.assertEqual(
            len(
                service.Equipment.Units.Service_Equipment_Units().load(
                    self.transfer.getUser()
                )
            ),
            2
        )

        self.controller.remove(self.transfer, {
            '_id': str(uDomain.getId())
        })

        self.assertEqual(
            len(
                service.Equipment.Units.Service_Equipment_Units().load(
                    self.transfer.getUser()
                )
            ),
            1
        )
