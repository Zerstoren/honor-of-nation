from . import AbstractService
import math


class AbstractEquipment(AbstractService.Service_Abstract):
    ACL = 'Acl.Equipment'
    PARAMS = 'Params.Equipment'
    JSONPACK = 'JsonPack.Equipment'

    JSONPACK_ACL = ['JsonPack.Equipment', 'Acl.Equipment']
    PARAMS_ACL = ['Params.Equipment', 'Acl.Equipment']
    PARAMS_JSONPACK = ['Params.Equipment', 'JsonPack.Equipment']
    PARAMS_JSONPACK_ACL = ['Params.Equipment', 'JsonPack.Equipment', 'Acl.Equipment']

    def _linearCalc(self, lvl, cost, degrage=False):
        if degrage:
            if lvl < 0:
                return 0

        return cost * lvl

    def _exponentCalc(self, lvl, cost, degrage=False, mod=1.0):
        if degrage:
            if lvl < 0:
                return 0

        if lvl == 0:
            return 0

        middleLevel = ((lvl + 1) * (float(lvl) / 2) / lvl / 1.000)
        expValue = middleLevel / 1000.0 * mod

        if expValue > 35:
            expValue = 35

        return (cost * math.exp(expValue)) * round(lvl, 5)
