from tests.backend.t_controller.equipment.generic import Backend_Controller_Equipment_Generic

import helpers.mongo
import helpers.math

from controller.EquipmentController import ArmorModelController, ArmorCollectionController
from models.Equipment.Armor.Factory import Equipment_Armor_Factory

import service.Equipment.Armor


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
        return ArmorModelController()

    def testGetModel(self):
        self.init()
        aDomain = self.createEquipmentArmor(
            self.transfer.getUser(),
            shield=(True, 'wood', 150, 20, )
        )

        self.controller.get(
            self.transfer,
            {
                '_id': str(aDomain.getId())
            }
        )

        result = self.transfer.getLastMessage()['message']
        self.assertTrue(result['done'])

        self.assertDictEqual(
            result['data'],
            {
                '_id': str(aDomain.getId()),
                'user': str(aDomain.getUser().getId()),
                'type': 'leather',
                'absorption': -10,
                'agility': 30,
                'eat': 3631,
                'health': 30,
                'level': 1,
                'rubins': 20174,
                'shield': True,
                'shield_type': 'wood',
                'shield_blocking': 20,
                'shield_durability': 150,
                'steel': 200,
                'time': 27,
                'wood': 5081
            }
        )

    def testLoadModel(self):
        self.init()
        aDomain1 = self.createEquipmentArmor(
            self.transfer.getUser()
        )

        aDomain2 = self.createEquipmentArmor(
            self.transfer.getUser(),
            aType='plate'
        )

        aDomain3 = self.createEquipmentArmor(
            self.fixture.getUser(3),
            aType='leather'
        )

        ArmorCollectionController().load(
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
            'type': 'mail',
            'user': str(self.transfer.getUser().getId()),
            'health': 0,
            'agility': 0,
            'absorption': 0,
            'shield': False,
            'shield_type': 0,
            'shield_durability': 0,
            'shield_blocking': 0
        })

        result = self.transfer.getLastMessage()['message']['data']

        armor = Equipment_Armor_Factory.get(
            helpers.mongo.objectId(result['_id'])
        )

        self.assertDictEqual(
            armor._domain_data,
            {
                '_id': armor.getId(),
                 'user': self.transfer.getUser().getId(),
                 'type': 'mail',

                 'health': 0,
                 'absorption': 0,
                 'agility': 0,

                 'shield': False,
                 'shield_blocking': False,
                 'shield_durability': False,
                 'shield_type': False,

                 'time': 5,
                 'level': 0,
                 'eat': 500,
                 'rubins': 3000,
                 'steel': 150,
                 'wood': 2000,
                 'remove': 0
            }
        )

    def testCreateBigNumbers(self):
        self.init()
        self.controller.save(self.transfer, {
            'type': 'plate',
            'user': str(self.transfer.getUser().getId()),

            'health': 5000,
            'agility': 220,
            'absorption': 120,

            'shield': True,
            'shield_type': 'wood',
            'shield_durability': 1200,
            'shield_blocking': 60
        })

        result = self.transfer.getLastMessage()['message']['data']
        armor = Equipment_Armor_Factory.get(
            helpers.mongo.objectId(result['_id'])
        )

        self.assertDictEqual(
            armor._domain_data,
            {
                '_id': armor.getId(),
                'user': self.transfer.getUser().getId(),

                'type': 'plate',

                'health': 5000,
                'absorption': 120,
                'agility': 220,

                'shield': True,
                'shield_type': 'wood',
                'shield_durability': 1200,
                'shield_blocking': 60,

                'time': 1567,
                'level': 75,
                'eat': 303173,
                'rubins': 1502024,
                'steel': 64053,
                'wood': 563179,

                'remove': 0
            }
        )

    def testSimulate(self):
        self.init()
        self.controller.save(self.transfer, {
            'type': 'plate',
            'user': str(self.transfer.getUser().getId()),
            'health': 5000,
            'agility': 220,
            'absorption': 120,

            'shield': True,
            'shield_type': 'wood',
            'shield_durability': 1200,
            'shield_blocking': 60
        })

        result = self.transfer.getLastMessage()['message']['data']
        armor = Equipment_Armor_Factory.get(
            helpers.mongo.objectId(result['_id'])
        )

        self.controller.simulate(self.transfer, {
            'type': 'plate',
            'health': 5000,
            'agility': 220,
            'absorption': 120,

            'shield': True,
            'shield_type': 'wood',
            'shield_durability': 1200,
            'shield_blocking': 60

        })
        result = self.transfer.getLastMessage()['message']['data']

        del armor._domain_data['user']
        del armor._domain_data['remove']
        del armor._domain_data['_id']
        del result['stamp']

        self.assertDictEqual(
            armor._domain_data,
            result
        )

    def testChangedValues(self):
        self.init()
        aDomain1 = self.createEquipmentArmor(
            self.transfer.getUser(),
            health=2
        )
        aDomain2 = self.createEquipmentArmor(
            self.transfer.getUser(),
            health=3
        )

        self.assertNotEqual(
            aDomain1.getRubins(),
            aDomain2.getRubins()
        )

    def testRemove(self):
        self.init()
        aDomain = self.createEquipmentArmor(
            self.transfer.getUser()
        )
        aDomain2 = self.createEquipmentArmor(
            self.transfer.getUser()
        )

        self.assertEqual(
            len(
                service.Equipment.Armor.Service_Equipment_Armor().load(
                    self.transfer.getUser()
                )
            ),
            2
        )

        self.controller.remove(self.transfer, {
            '_id': str(aDomain.getId())
        })

        self.assertEqual(
            len(
                service.Equipment.Armor.Service_Equipment_Armor().load(
                    self.transfer.getUser()
                )
            ),
            1
        )