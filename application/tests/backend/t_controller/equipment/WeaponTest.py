from tests.backend.t_controller.equipment.generic import Backend_Controller_Equipment_Generic

import helpers.mongo
import helpers.math

from controller.EquipmentController import WeaponModelController, WeaponCollectionController
from models.Equipment.Weapon.Factory import Equipment_Weapon_Factory

import service.Equipment.Weapon


class Backend_Controller_AdminTest(Backend_Controller_Equipment_Generic):
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
        return WeaponModelController()

    def testGetModel(self):
        self.init()
        wDomain = self.createEquipmentWeapon(
            self.transfer.getUser()
        )

        self.controller.get(
            self.transfer,
            {
                '_id': str(wDomain.getId())
            }
        )

        result = self.transfer.getLastMessage()['message']
        self.assertTrue(result['done'])
        self.assertDictEqual(
            result['data'],
            {
                '_id': str(wDomain.getId()),
                'user': str(wDomain.getUser().getId()),
                'type': 'sword',
                'damage': 100,
                'speed': 40,
                'critical_chance': 5,
                'critical_damage': 2.0,
                'eat': 55651,
                'rubins': 255095,
                'steel': 110906,
                'wood': 17092,
                'level': 16,
                'time': 87
            }
        )

    def testLoadModel(self):
        self.init()
        wDomain1 = self.createEquipmentWeapon(
            self.transfer.getUser()
        )
        wDomain2 = self.createEquipmentWeapon(
            self.transfer.getUser(),
            wType='spear'
        )

        wDomain3 = self.createEquipmentWeapon(
            self.fixture.getUser(3),
            wType='bow'
        )

        WeaponCollectionController().load(
            self.transfer,
            {
                'user': str(self.transfer.getUser().getId())
            }
        )

        result = self.transfer.getLastMessage()['message']
        self.assertEqual(len(result['data']), 2)

    def testCreateBase(self):
        self.init()
        self.controller.save(self.transfer, {
            'type': 'sword',
            'user': str(self.transfer.getUser().getId()),
            'damage': 0,
            'speed': 0,
            'critical_chance': 0,
            'critical_damage': 0
        })

        result = self.transfer.getLastMessage()['message']
        weapon = Equipment_Weapon_Factory.get(
            helpers.mongo.objectId(result['_id'])
        )

        self.assertDictEqual(
            weapon._domain_data,
            {
                '_id': weapon.getId(),
                 'user': self.transfer.getUser().getId(),
                 'critical_chance': 0,
                 'critical_damage': 0.0,
                 'damage': 0,
                 'eat': 500,
                 'level': 0,
                 'remove': 0,
                 'rubins': 3000,
                 'speed': 0,
                 'time': 5,
                 'steel': 150,
                 'type': 'sword',
                 'wood': 2000
            }
        )

    def testCreateBigNumbers(self):
        self.init()
        self.controller.save(self.transfer, {
            'type': 'sword',
            'user': str(self.transfer.getUser().getId()),
            'damage': '12000',
            'speed': 900.9,
            'critical_chance': 14,
            'critical_damage': 3
        })

        result = self.transfer.getLastMessage()['message']
        weapon = Equipment_Weapon_Factory.get(
            helpers.mongo.objectId(result['_id'])
        )

        self.assertDictEqual(
            weapon._domain_data,
            {
                '_id': weapon.getId(),
                 'user': self.transfer.getUser().getId(),
                 'critical_chance': 14,
                 'critical_damage': 3.0,
                 'type': 'sword',
                 'damage': 12000,
                 'eat': 379653814,
                 'level': 90322,
                 'remove': 0,
                 'time': 474581,
                 'rubins': 1614782853,
                 'speed': 900,
                 'steel': 948443356,
                 'wood': 47738295
            }
        )

    def testSimulate(self):
        self.init()
        self.controller.save(self.transfer, {
            'type': 'sword',
            'user': str(self.transfer.getUser().getId()),
            'damage': '12000',
            'speed': 900.9,
            'critical_chance': 14,
            'critical_damage': 3
        })

        result = self.transfer.getLastMessage()['message']
        weapon = Equipment_Weapon_Factory.get(
            helpers.mongo.objectId(result['_id'])
        )


        self.controller.simulate(self.transfer, {
            'type': 'sword',
            'damage': '12000',
            'speed': 900.9,
            'critical_chance': 14,
            'critical_damage': 3
        })
        result = self.transfer.getLastMessage()['message']['data']

        del weapon._domain_data['user']
        del weapon._domain_data['remove']
        del weapon._domain_data['_id']

        self.assertDictEqual(
            weapon._domain_data,
            result
        )

    def testChangedValues(self):
        self.init()
        wDomain1 = self.createEquipmentWeapon(
            self.transfer.getUser(),
            critical_damage=2.0
        )
        wDomain2 = self.createEquipmentWeapon(
            self.transfer.getUser(),
            critical_damage=3.0
        )

        self.assertNotEqual(
            wDomain1.getRubins(),
            wDomain2.getRubins()
        )

    def testRemove(self):
        self.init()
        wDomain = self.createEquipmentWeapon(
            self.transfer.getUser()
        )
        wDomain2 = self.createEquipmentWeapon(
            self.transfer.getUser()
        )

        self.assertEqual(
            len(
                service.Equipment.Weapon.Service_Equipment_Weapon().load(
                    self.transfer.getUser()
                )
            ),
            2
        )

        self.controller.remove(self.transfer, {
            '_id': str(wDomain.getId())
        })

        self.assertEqual(
            len(
                service.Equipment.Weapon.Service_Equipment_Weapon().load(
                    self.transfer.getUser()
                )
            ),
            1
        )