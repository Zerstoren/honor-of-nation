from service.Army import Service_Army
from service.ArmyQueue import Service_ArmyQueue

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
