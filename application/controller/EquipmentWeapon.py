from service.Equipment.Weapon import Service_Equipment_Weapon

class _AbstractController(object):
    def _getParamsEquipmentService(self):
        return Service_Equipment_Weapon().decorate('Params.Equipment')

    def _getParamsJsonPackEquipmentWeaponService(self):
        return Service_Equipment_Weapon().decorate('Params.Equipment', 'JsonPack.Equipment')

    def _getParamsJsonPackAclEquipmentWeaponService(self):
        return Service_Equipment_Weapon().decorate('Params.Equipment', 'JsonPack.Equipment', 'Acl.Equipment')

class ModelController(_AbstractController):
    def simulate(self, transfer, data):
        service = self._getParamsJsonPackEquipmentWeaponService()
        weaponData = service.simulate(data)

        transfer.send('/model/equipment/simulate', {
            'done': True,
            'data': weaponData
        })

    def save(self, transfer, data):
        service = self._getParamsEquipmentService()
        domain = service.save(data)

        transfer.send('/model/equipment/save', {
            'done': True,
            '_id': str(domain.getId())
        })

    def get(self, transfer, data):
        service = self._getParamsJsonPackAclEquipmentWeaponService()
        weaponData = service.get(data['_id'], transfer.getUser())

        transfer.send('/model/equipment/get', {
            'done': True,
            'data': weaponData
        })

    def load(self, transfer, data):
        service = self._getParamsJsonPackEquipmentWeaponService()
        weaponData = service.load(data['user'])

        transfer.send('/model/equipment/load', {
            'done': True,
            'data': weaponData
        })