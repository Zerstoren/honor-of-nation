from .Abstract import AbstractService

from models.Army.Domain import Army_Domain
from models.Army.Factory import Army_Factory

from models.Equipment.Units import Common
from models.Map import Data as Map_Data
from models.Army import Common as Army_Common

from service.Town import Service_Town
from service.Map import Service_Map

import exceptions.army
import helpers.MapCoordinate

import init_celery
import config
import time


class Service_Army(AbstractService.Service_Abstract):
    def create(self, unit, town, count, user=None):
        return self._create(unit, town, count)

    def get(self, _id, user=None):
        return Army_Factory.get(_id)

    def loadByMapCollection(self, collection):
        """
        :type collection: collection.MapCollection.Map_Collection
        """
        return Army_Factory.loadByMapCollection(collection)

    def load(self, armyUser, position, config=None, user=None):
        if config is None:
            config = dict()

        detail = config['detail'] if 'detail' in config else False
        inBuild = config['inBuild'] if 'inBuild' in config else None

        return Army_Factory.getByPosition(armyUser, position, detail=detail, inBuild=inBuild)

    def loadDetail(self, armyUser, _id, user=None):
        def load(leader):
            suite = leader.getSuite()
            army = Army_Factory.getCollectionByGeneral(leader)

            armyData = []

            for domain in army:
                if not suite or suite.getId() != domain.getId():
                    armyData.append(load(domain))

            return {
                'current': leader,
                'suite': suite,
                'sub_army': armyData
            }

        commander = Army_Factory.get(_id)
        return load(commander)

    def changeMoveType(self, general, move, user=None):
        pass

    def addSuite(self, generalArmy, solidersArmy, user=None):
        if generalArmy.getUnit().getType() != Common.TYPE_GENERAL:
            raise exceptions.army.CommanderNotPermission("Недопустимая операция для командира")

        if solidersArmy.getUnit().getType() != Common.TYPE_SOLIDER:
            raise exceptions.army.UnitNotPermission("Недопустимая операция для солдатов")

        if generalArmy.getSuite():
            raise exceptions.army.Suite("Генерал уже имеет свиту")

        if solidersArmy.getCommander():
            raise exceptions.army.Suite("Солдат уже подвязан к командиру")

        if generalArmy.getInBuild() is not True or solidersArmy.getInBuild() is not True:
            raise exceptions.army.UnitNotInBuild("Юнит обязан находится в городе")

        size = self._calculateUnitsSize(generalArmy) + solidersArmy.getCount()
        if size > generalArmy.getUnit().getTroopSize():
            raise exceptions.army.ArmyLimit("Командир не может управлять большей армией")

        solidersArmy.setCommander(generalArmy)
        solidersArmy.getMapper().save(solidersArmy)

        generalArmy.setSuite(solidersArmy)
        generalArmy.getMapper().save(generalArmy)

    def removeSuite(self, generalArmy, solidersArmy, user=None):
        if generalArmy.getUnit().getType() != Common.TYPE_GENERAL:
            raise exceptions.army.CommanderNotPermission("Недопустимая операция для командира")

        if solidersArmy.getUnit().getType() != Common.TYPE_SOLIDER:
            raise exceptions.army.UnitNotPermission("Недопустимая операция для солдатов")

        if not generalArmy.getSuite():
            raise exceptions.army.Suite("Генерал не имеет свиты")

        if solidersArmy.getCommander() and solidersArmy.getCommander().getId() != generalArmy.getId():
            raise exceptions.army.Suite("Солдат уже подвязан к другому командиру")

        generalArmy.setSuite(None)
        generalArmy.getMapper().save(generalArmy)

        solidersArmy.setCommander(None)
        solidersArmy.getMapper().save(solidersArmy)

    def addSolidersToGeneral(self, generalArmy, solidersCollection, user=None):
        solidersSize = 0

        if generalArmy.getUnit().getType() != Common.TYPE_GENERAL:
            raise exceptions.army.WrongArgument("Должен быть генерал")

        for army in solidersCollection:
            if army.getCommander() is not None:
                raise exceptions.army.UnitHasCommander("Юнит уже имеет командира")

            if army.getMap().getPosition().getPosId() != generalArmy.getMap().getPosition().getPosId():
                raise exceptions.army.AddSolidersToUnit("Юнит находится на неверной позиции относительно командира")

            if army.getInBuild() is False:
                raise exceptions.army.UnitNotInBuild("Юнит не находится в здании")

            if army.getUnit().getType() == Common.TYPE_GENERAL:
                if self._hasDeepGeneral(army) or generalArmy.getCommander():
                    raise exceptions.army.AddSolidersToUnit("Нельзя создавать цепочку из 3х генералов")

            solidersSize += self._calculateUnitsSize(army)

        if self._calculateUnitsSize(generalArmy) + solidersSize > generalArmy.getUnit().getTroopSize():
            raise exceptions.army.ArmyLimit("Командир не может управлять большей армией")

        for army in solidersCollection:
            army.setCommander(generalArmy)
            army.getMapper().save(army)

    def removeSolidersFromGeneral(self, generalArmy, solidersCollection, user=None):
        if generalArmy.getUnit().getType() != Common.TYPE_GENERAL:
            raise exceptions.army.WrongArgument("Должен быть генерал")

        if generalArmy.getInBuild() is False:
            raise exceptions.army.UnitNotInBuild("Юнит не находится в здании")

        for army in solidersCollection:
            if army.getCommander() is None:
                raise exceptions.army.UnitHasNotCommander("Юнит уже не имеет командира")

            if army.getInBuild() is False:
                raise exceptions.army.UnitNotInBuild("Юнит не находится в здании")

        for army in solidersCollection:
            army.setCommander(None)
            army.getMapper().save(army)

    def moveInBuild(self, armyDomain, user=None):
        if armyDomain.getInBuild() is True:
            raise exceptions.army.UnitNotInBuild("Юнит обязан находится вне городе")

        armyDomain.setInBuild(True)
        armyDomain.getMapper().save(armyDomain)

    def moveOutBuild(self, armyDomain, user=None):
        if armyDomain.getUnit().getType() == Common.TYPE_SOLIDER:
            raise exceptions.army.UnitNotPermission("Солдаты не могут самостоятельно выходить из строений")

        if armyDomain.getInBuild() is False:
            raise exceptions.army.UnitNotInBuild("Юнит обязан находится в городе")

        armyDomain.setInBuild(False)
        armyDomain.getMapper().save(armyDomain)

    def merge(self, armyCollection, user=None):
        armyBase = armyCollection[0]
        resultCount = armyBase.getCount()

        for domain in armyCollection:
            if domain.getUnit().getType() == Common.TYPE_GENERAL:
                raise exceptions.army.CommanderNotPermission("Недопустимая операция для командира")

            if domain.getCommander() != None:
                raise exceptions.army.UnitHasCommander("Юнит имеет командира и не может провести операцию")

            if domain.getInBuild() is not True:
                raise exceptions.army.UnitNotInBuild("Юнит обязан находится в городе")

        for i in range(1, len(armyCollection)):
            armyCurrent = armyCollection[i]
            if armyBase.getUnit().getId() != armyCurrent.getUnit().getId():
                raise exceptions.army.Merge("Армии имеют разные типы юнитов")

            if armyBase.getMap().getPosition().getPosId() != armyCurrent.getMap().getPosition().getPosId():
                raise exceptions.army.Merge("Армии находятся на разных позициях")

            resultCount += armyCurrent.getCount()
            armyCurrent.getMapper().remove(armyCurrent)

        armyBase.setCount(resultCount)
        armyBase.getMapper().save(armyBase)

    def split(self, armyDomain, size, user=None):
        if armyDomain.getUnit().getType() == Common.TYPE_GENERAL:
            raise exceptions.army.CommanderNotPermission("Недопустимая операция для командира")

        if armyDomain.getCommander() is not None:
            raise exceptions.army.UnitHasCommander("Юнит имеет командира и не может провести операцию")

        if armyDomain.getInBuild() is not True:
            raise exceptions.army.UnitNotInBuild("Юнит обязан находится в городе")

        if armyDomain.getCount() <= size or size <= 0:
            raise exceptions.army.Split("Неверный размер для разделения")

        self._create(
            armyDomain.getUnit(),
            Service_Town().loadByPosition(armyDomain.getMap().getPosition()),
            size
        )

        armyDomain.setCount(armyDomain.getCount() - size)
        armyDomain.getMapper().save(armyDomain)

    def dissolution(self, armyDomain, user=None):
        if armyDomain.getInBuild() is not True:
            raise exceptions.army.UnitNotInBuild("Юнит обязан находится в городе")

        if armyDomain.getCommander() is not None:
            raise exceptions.army.UnitHasCommander("Юнит имеет командира и не может провести операцию")

        if armyDomain.getSuite() is not None:
            raise exceptions.army.CommanderNotPermission("Командир имеет свиту")

        armyDomain.getMapper().remove(armyDomain)

    def _calculateUnitsSize(self, armyDomain):
        size = 0

        if armyDomain.getUnit().getType() == Common.TYPE_SOLIDER:
            return armyDomain.getCount()

        suiteArmy = armyDomain.getSuite()
        if suiteArmy:
            size += suiteArmy.getCount()

        armyCollection = Army_Factory.getCollectionByGeneral(armyDomain)

        for army in armyCollection:
            if army.getUnit().getType() == Common.TYPE_GENERAL:
                size += self._calculateUnitsSize(army)
                continue

            size += army.getCount()

        return size

    def _hasDeepGeneral(self, armyDomain):
        collection = Army_Factory.getSubGenerals(armyDomain)
        return bool(len(collection))

    def _create(self, unit, town, count):
        domain = Army_Domain()
        domain.setUnit(unit)
        domain.setUser(town.getUser())
        domain.setCount(count)
        domain.setCommander(None)
        domain.setMap(town.getMap())
        domain.setInBuild(True)
        domain.setPower(100)
        domain.setMode(1)
        domain.setMovePath([])
        domain.setFormation(None)
        domain.setSuite(None)
        domain.setIsGeneral(unit.getType() == Common.TYPE_GENERAL)
        domain.setLastPowerUpdate(int(time.time()))

        domain.getMapper().save(domain)
        return domain

    def move(self, general, mapPath, user=None):
        items = general.getMovePath()
        if len(items) > 0 and 'code' in items[0]:
            init_celery.app.control.revoke(items[0]['code'])


        general.setMovePath(mapPath)
        self._updatePathMove(general)

    def _moveUnitPosition(self, general):
        path = general.getMovePath()
        if len(path) and 'code' in path[0] and path[0]['start_at'] + path[0]['complete_after'] >= int(time.time()):
            pathItem = path.pop(0)
            general.setPower(general.getPower() - pathItem['power'])
            general.setLocation(pathItem['pos_id'])
            general.setMovePath(path)

            import controller.ArmyController
            controller.ArmyController.DeliveryController().moveUnit(general)

            return True

        if len(path) == 0:
            general.setMovePath([])
            general.getMapper().save(general)

        return False

    def updatePathMove(self, general):
        return self._updatePathMove(general)

    def _updatePathMove(self, general):
        self._moveUnitPosition(general)

        path = general.getMovePath()

        if len(path) == 0 or 'code' in path[0]:
            return

        mapCoordinate = Service_Map().getByPosition(helpers.MapCoordinate.MapCoordinate(posId=path[0]['pos_id']))
        waitForMove = int(config.get('army.infantry.base_wait'))
        powerPerSeconds = float(config.get('army.infantry.power_restore'))
        powerMove = Map_Data.MOVE['infantry']['byroad'][mapCoordinate.getLand()] - round(powerPerSeconds * int(waitForMove))
        armyPower = general.getPower()

        if general.getMode() == Army_Common.MODE_VERY_FAST:
            if powerMove > armyPower: # Restore all needed power to move
                waitForMove += round((powerMove - armyPower) / powerPerSeconds)
            else: # Do nothing, all info already calculated
                pass

        elif general.getMode() == Army_Common.MODE_FAST:
            if powerMove >= 20 and powerMove <= armyPower:
                waitForMove += round((powerMove - 20) / powerPerSeconds)
            elif powerMove <= armyPower and powerMove <= 20:
                pass # Do nothing, all info already calculated
            elif powerMove > armyPower: # Restore all needed power to move
                waitForMove += round((powerMove - armyPower) / powerPerSeconds)

        elif general.getMode() == Army_Common.MODE_NORMAL:
            if powerMove >= 10 and powerMove <= armyPower:
                waitForMove += round((powerMove - 10) / powerPerSeconds)
            elif powerMove <= armyPower and powerMove <= 10:
                pass # Do nothing, all info already calculated
            elif powerMove > armyPower: # Restore all needed power to move
                waitForMove += round((powerMove - armyPower) / powerPerSeconds)

        elif general.getMode() == Army_Common.MODE_SLOW:
            waitForMove += round(int(100 - (armyPower - powerMove)) / powerPerSeconds)

        queueMessage = {
            'general': str(general.getId()),
            'power': Map_Data.MOVE['infantry']['byroad'][mapCoordinate.getLand()],
            'complete_after': waitForMove,
            'start_at': int(time.time())
        }

        path[0]['code'] = str(init_celery.army_move.apply_async((queueMessage, ), countdown=queueMessage['complete_after']))
        path[0]['power'] = queueMessage['power']
        path[0]['start_at'] = queueMessage['start_at']
        path[0]['complete_after'] = queueMessage['complete_after']

        general.setMovePath(path)
        general.getMapper().save(general)


    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_Army
        """
        return super().decorate(*args)
