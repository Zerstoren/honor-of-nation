from service.Army import Service_Army
from service.MapUserVisible import Service_MapUserVisible


class _AbstractArmy(object):
    def _getParamsAclService(self):
        return Service_Army().decorate(Service_Army.PARAMS_ACL)

    def _getParamsArmyService(self):
        return Service_Army().decorate(Service_Army.PARAMS_JSONPACK_ACL)



class MainController(_AbstractArmy):
    def detail(self, transfer, data):
        result = self._getParamsArmyService().loadDetail(
            data['user'],
            data['army'],
            transfer.getUser()
        )

        result['done'] = True
        transfer.send('/army/detail', result)

    def move(self, transfer, data):
        self._getParamsAclService().move(
            data['army_id'],
            data['path'],
            transfer.getUser()
        )

    def mode(self, transfer, data):
        pass

    def moveInBuild(self, transfer, data):
        self._getParamsAclService().moveInBuild(
            data['army'],
            transfer.getUser()
        )

        transfer.send('/army/in_build', {
            'done': True
        })

    def moveOutBuild(self, transfer, data):
        self._getParamsAclService().moveOutBuild(
            data['army'],
            transfer.getUser()
        )

        transfer.send('/army/out_build', {
            'done': True
        })

    def merge(self, transfer, data):
        self._getParamsAclService().merge(
            data['army_list'],
            transfer.getUser()
        )

        transfer.send('/army/merge', {
            'done': True
        })

    def split(self, transfer, data):
        self._getParamsAclService().split(
            data['army'],
            data['size'],
            transfer.getUser()
        )

        transfer.send('/army/split', {
            'done': True
        })

    def addSolidersToGeneral(self, transfer, data):
        self._getParamsAclService().addSolidersToGeneral(
            data['general'],
            data['soliders'],
            transfer.getUser()
        )

        transfer.send('/army/add_soliders_general', {
            'done': True
        })

    def removeSolidersGeneral(self, transfer, data):
        self._getParamsAclService().removeSolidersFromGeneral(
            data['general'],
            data['soliders'],
            transfer.getUser()
        )

        transfer.send('/army/remove_soliders_general', {
            'done': True
        })

    def addSuite(self, transfer, data):
        self._getParamsAclService().addSuite(
            data['general'],
            data['solider'],
            transfer.getUser()
        )

        transfer.send('/army/add_suite', {
            'done': True
        })

    def removeSuite(self, transfer, data):
        self._getParamsAclService().removeSuite(
            data['general'],
            data['solider'],
            transfer.getUser()
        )

        transfer.send('/army/remove_suite', {
            'done': True
        })

    def dissolution(self, transfer, data):
        self._getParamsAclService().dissolution(
            data['army'],
            transfer.getUser()
        )

        transfer.send('/army/dissolution', {
            'done': True
        })


class CollectionController(_AbstractArmy):
    def load(self, transfer, data):
        config = data['config'] if 'config' in data else None
        result = self._getParamsArmyService().load(
            data['user'],
            data['pos_id'],
            config=config,
            user=transfer.getUser()
        )

        transfer.send('/collection/army/load', {
            'done': True,
            'data': result
        })


class CeleryPrivateController(_AbstractArmy):
    def updateMove(self, message):
        #{'general': '54f080c7608fb34ac60f1326', 'complete_after': 5, 'power': 8, 'start_at': 1425047751}
        self._getParamsArmyService().updatePathMove(message['general'])


class DeliveryController(_AbstractArmy):
    def updateUnitsOnMap(self, user, unitsList):
        user.getTransfer().forceSend('/delivery/unitsUpdateOnMap', {
            'done': True,
            'units': unitsList
        })

    def moveUnit(self, general):
        posId = general.getLocation()
        Service_MapUserVisible()
