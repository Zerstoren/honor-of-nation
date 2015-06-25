from service.Army import Service_Army
from service.ArmyQueue import Service_ArmyQueue
from helpers.MapCoordinate import MapCoordinate

class Army(object):
    def createArmy(
        self,
        town,
        unit,
        count=100
    ):
        return Service_Army().create(
            unit,
            town,
            count
        )

    def createArmyQueue(
        self,
        town,
        unit,
        count=10
    ):
        return Service_ArmyQueue().add(
            town,
            unit,
            count,
            town.getUser()
        )

    def setArmySoliderToGeneral(self, solider, general):
        solider.setCommander(general)
        solider.getMapper().save(solider)

    def setArmySuiteToGeneral(self, solider, general):
        general.setSuite(solider)
        general.getMapper().save(general)

    def setArmyLeaveTown(self, general):
        general.setInBuild(False)
        general.getMapper().save(general)

    def fastMove(self, general, x, y):
        general.setMovePath([
            {
                'pos_id': MapCoordinate(x=x, y=y).getPosId(),
                'direction': '',
                'code': '',
                'power': 0,
                'start_at': 0,
                'complete_after': 1
            }
        ])

        general.getMapper().save(general)

        Service_Army()._moveUnitPosition(general)
