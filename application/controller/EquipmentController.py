from service.Equipment.Weapon import Service_Equipment_Weapon

import time


class _AbstractWeaponController(object):
    def _getParamsEquipmentService(self):
        return Service_Equipment_Weapon().decorate('Params.Equipment')

    def _getParamsJsonPackEquipmentWeaponService(self):
        return Service_Equipment_Weapon().decorate('Params.Equipment', 'JsonPack.Equipment')

    def _getParamsJsonPackAclEquipmentWeaponService(self):
        return Service_Equipment_Weapon().decorate('Params.Equipment', 'JsonPack.Equipment', 'Acl.Equipment')


class _AbstractArmorController(object):
    pass


class WeaponModelController(_AbstractWeaponController):
    def simulate(self, transfer, data):
        service = self._getParamsJsonPackEquipmentWeaponService()
        weaponData = service.simulate(data)
        weaponData['stamp'] = time.time()

        transfer.send('/model/equipment/weapon/simulate', {
            'done': True,
            'data': weaponData
        })

    def save(self, transfer, data):
        service = self._getParamsJsonPackEquipmentWeaponService()
        data = service.save(data, transfer.getUser())

        transfer.send('/model/equipment/weapon/save', {
            'data': data,
            'done': True
        })

    def get(self, transfer, data):
        service = self._getParamsJsonPackAclEquipmentWeaponService()
        weaponData = service.get(data['_id'], transfer.getUser())

        transfer.send('/model/equipment/weapon/get', {
            'done': True,
            'data': weaponData
        })

    def remove(self, transfer, data):
        service = self._getParamsJsonPackAclEquipmentWeaponService()
        service.remove(data['_id'], transfer.getUser())

        transfer.send('/model/equipment/weapon/remove', {
            'done': True
        })


class WeaponCollectionController(_AbstractWeaponController):
    def load(self, transfer, data):
        service = self._getParamsJsonPackEquipmentWeaponService()
        weaponData = service.load(data['user'])

        transfer.send('/collection/equipment/weapon/load', {
            'done': True,
            'data': weaponData
        })


class ArmorModelController(_AbstractArmorController):
    pass


class ArmorCollectionController(_AbstractArmorController):
    pass
