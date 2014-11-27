from tests.backend.t_controller.equipment.generic import Backend_Controller_Equipment_Generic

import helpers.mongo
import helpers.math

from controller.EquipmentWeapon import ModelController
from models.Equipment.Weapon.Factory import Equipment_Weapon_Factory


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
        return ModelController()

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
                'level': 10,
                'rubins': 134999,
                'damage': 100,
                'speed': 40,
                'time': 39,
                'critical_chance': 5,
                'wood': 11087,
                'critical_damage': 2,
                'steel': 50858,
                'eat': 25627
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

        self.controller.load(
            self.transfer,
            {
                'user': str(self.transfer.getUser().getId())
            }
        )

        result = self.transfer.getLastMessage()['message']

        example = {
            'done': True,
            'data': [
                {
                    '_id': str(wDomain1.getId()),
                    'user': str(self.transfer.getUser().getId()),
                    'type': 'sword',
                    'wood': 11087,
                    'eat': 25627,
                    'level': 10,
                    'time': 39,
                    'steel': 50858,
                    'damage': 100,
                    'critical_damage': 2,
                    'rubins': 134999,
                    'speed': 40,
                    'critical_chance': 5
                },
                {
                    '_id': str(wDomain2.getId()),
                    'user': str(self.transfer.getUser().getId()),
                    'type': 'spear',
                    'wood': 16872,
                    'eat': 34701,
                    'level': 14,
                    'time': 47,
                    'steel': 65132,
                    'damage': 100,
                    'critical_damage': 2,
                    'rubins': 175527,
                    'speed': 40,
                    'critical_chance': 5
                }
            ]
        }

        self.assertDictEqual(
            result,
            example
        )

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
