from service.Equipment.Weapon import Service_Equipment_Weapon
from service.Equipment.Armor import Service_Equipment_Armor

import time


class _AbstractWeaponController(object):
    def _getParamsEquipmentService(self):
        return Service_Equipment_Weapon().decorate(Service_Equipment_Weapon.PARAMS)

    def _getParamsJsonPackEquipmentWeaponService(self):
        return Service_Equipment_Weapon().decorate(Service_Equipment_Weapon.PARAMS_JSONPACK)

    def _getParamsJsonPackAclEquipmentWeaponService(self):
        return Service_Equipment_Weapon().decorate(Service_Equipment_Weapon.PARAMS_JSONPACK_ACL)


class _AbstractArmorController(object):
    def _getParamsEquipmentService(self):
        return Service_Equipment_Armor().decorate(Service_Equipment_Armor.PARAMS)

    def _getParamsJsonPackEquipmentArmorService(self):
        return Service_Equipment_Armor().decorate(Service_Equipment_Armor.PARAMS_JSONPACK)

    def _getParamsJsonPackAclEquipmentArmorService(self):
        return Service_Equipment_Armor().decorate(Service_Equipment_Armor.PARAMS_JSONPACK_ACL)


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
    def simulate(self, transfer, data):
        service = self._getParamsJsonPackEquipmentArmorService()
        armorData = service.simulate(data)
        armorData['stamp'] = time.time()

        transfer.send('/model/equipment/armor/simulate', {
            'done': True,
            'data': armorData
        })

    def save(self, transfer, data):
        service = self._getParamsJsonPackEquipmentArmorService()
        data = service.save(data, transfer.getUser())

        transfer.send('/model/equipment/armor/save', {
            'data': data,
            'done': True
        })

    def get(self, transfer, data):
        service = self._getParamsJsonPackAclEquipmentArmorService()
        armorData = service.get(data['_id'], transfer.getUser())

        transfer.send('/model/equipment/armor/get', {
            'done': True,
            'data': armorData
        })

    def remove(self, transfer, data):
        service = self._getParamsJsonPackAclEquipmentArmorService()
        service.remove(data['_id'], transfer.getUser())

        transfer.send('/model/equipment/armor/remove', {
            'done': True
        })


class ArmorCollectionController(_AbstractArmorController):
    def load(self, transfer, data):
        service = self._getParamsJsonPackEquipmentArmorService()
        armorData = service.load(data['user'])

        transfer.send('/collection/equipment/armor/load', {
            'done': True,
            'data': armorData
        })
