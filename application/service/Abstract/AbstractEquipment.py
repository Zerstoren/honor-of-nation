from . import AbstractService
import math


class AbstractEquipment(AbstractService.Service_Abstract):
    ACL = 'Acl.Equipment'
    PARAMS = 'Params.Equipment'
    JSON_PACK = 'JsonPack.Equipment'

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
        return (cost * math.exp(middleLevel / 1000.0 * mod)) * lvl
