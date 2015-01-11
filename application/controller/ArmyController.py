from service.Army import Service_Army


class _AbstractArmy(object):
    def _getParamsArmyService(self):
        return Service_Army().decorate(Service_Army.PARAMS_JSONPACK_ACL)


class MainController(_AbstractArmy):
    pass


class CollectionController(_AbstractArmy):
    def load(self, transfer, data):
        result = self._getParamsArmyService().load(
            data['user'],
            data['pos_id'],
            transfer.getUser()
        )

        transfer.send('/collection/army/load', {
            'done': True,
            'data': result
        })
