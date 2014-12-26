from service.Equipment.Units import Service_Equipment_Units

import time


class _AbstractController(object):
    def _getParamsJsonPackEquipmentService(self):
        return Service_Equipment_Units().decorate('Params.Equipment', 'JsonPack.Equipment')

    def _getParamsJsonPackAclEquipmentService(self):
        return Service_Equipment_Units().decorate('Params.Equipment', 'JsonPack.Equipment', 'Acl.Equipment')


class UnitsModelController(_AbstractController):
    def simulate(self, transfer, data):
        service = self._getParamsJsonPackEquipmentService()
        unitData = service.simulate(data)
        unitData['stamp'] = time.time()

        transfer.send('/model/equipment/unit/simulate', {
            'done': True,
            'data': unitData
        })

    def save(self, transfer, data):
        service = self._getParamsJsonPackEquipmentService()
        data = service.save(data, transfer.getUser())

        transfer.send('/model/equipment/unit/save', {
            'data': data,
            'done': True
        })

    def get(self, transfer, data):
        service = self._getParamsJsonPackAclEquipmentService()

        transfer.send('/model/equipment/unit/get', {
            'done': True,
            'data': service.get(data['_id'], transfer.getUser())
        })

    def remove(self, transfer, data):
        service = self._getParamsJsonPackAclEquipmentService()
        service.remove(data['_id'], transfer.getUser())

        transfer.send('/model/equipment/unit/remove', {
            'done': True
        })


class UnitsCollectionController(_AbstractController):
    def load(self, transfer, data):
        service = self._getParamsJsonPackEquipmentService()

        transfer.send('/collection/equipment/armor/load', {
            'done': True,
            'data': service.load(data['user'])
        })
