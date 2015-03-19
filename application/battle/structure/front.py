from battle.simulate import rand
import  helpers.math


class FrontCollection(object):
    avangard = None
    leftFlang = None
    rightFlang = None
    rear = None
    location = None

    def __init__(self, inDefence):
        self.inDefence = inDefence

    def get(self, name):
        """
        :rtype: Front
        """
        if name == Front.TYPE_AVANGARD:
            return self.avangard
        elif name == Front.TYPE_LEFT_FLANG:
            return self.leftFlang
        elif name == Front.TYPE_RIGHT_FLANG:
            return self.rightFlang
        elif name == Front.TYPE_REAR:
            return self.rear

    def parseAction(self, sequence, enemyFrontCollection, myFront):
        """
        :type sequence: set
        :type enemyFrontCollection: FrontCollection
        :type myFront: Front
        """

        if myFront.getMeleeCount() == 0:
            return False

        if type(sequence) is set:
            for direction in sequence:
                if enemyFrontCollection.get(direction).getUnitsCount():
                    myFront.setTarget(enemyFrontCollection.get(direction))
                    return True

            return False
        else:
            for myDirection in sequence:
                if self.get(sequence[myDirection]).getUnitsCount() == 0:
                    return self.parseAction(sequence[myDirection], enemyFrontCollection, myFront)

    def getNextTarget(self, frontName, enemyFrontCollection):
        """
        :type frontName: string
        :type enemyFrontCollection: FrontCollection
        """
        myFront = self.get(frontName)
        if myFront and myFront.getTarget() and myFront.getTarget().getUnitsCount():
            return myFront.getTarget()
        else:
            if self.inDefence:
                sequence = self.location.getSequenceOfStrategicActionsDefender()
            else:
                sequence = self.location.getSequenceOfStrategicActionsAttacker()

            self.parseAction(sequence[frontName], enemyFrontCollection, myFront)

    def getArcheryTarget(self):
        """Used by enemy"""
        avangardSize = self.avangard.getUnitsCount()
        leftFlang = self.leftFlang.getUnitsCount()
        rightFlang = self.rightFlang.getUnitsCount()
        target = None
        count = 0

        if avangardSize >= count and not self.avangard.isBussy():
            target = self.avangard
            count = avangardSize

        if leftFlang >= count and not self.leftFlang.isBussy():
            target = self.leftFlang
            count = leftFlang

        if rightFlang >= count and not self.rightFlang.isBussy():
            target = self.rightFlang

        return target

    def iterateAll(self):
        for i in [self.avangard, self.leftFlang, self.rightFlang, self.rear]:
            yield i

    def getArmySize(self):
        armySize = 0
        for front in Front.TYPES:
            armySize += self.get(front).getUnitsCount()

        return armySize

    def setAvangard(self, front):
        """
        :type front: Front
        """
        front.setInDefence(self.inDefence)
        self.avangard = front

    def setLeftFlang(self, front):
        """
        :type front: Front
        """
        self.leftFlang = front

    def setRightFlang(self, front):
        """
        :type front: Front
        """
        self.rightFlang = front

    def setRear(self, front):
        """
        :type front: Front
        """
        self.rear = front

    def setLocation(self, location):
        self.location = location
        self.avangard.setLocation(location)
        self.leftFlang.setLocation(location)
        self.rightFlang.setLocation(location)
        self.rear.setLocation(location)


class Front(object):
    TYPE_AVANGARD = 1
    TYPE_LEFT_FLANG = 2
    TYPE_RIGHT_FLANG = 3
    TYPE_REAR = 4

    TYPES = (1, 2, 3, 4, )

    location = None
    inDefence = None

    currentFrontTarget = None
    currentWaitToMove = 0

    def __init__(self, frontDirection):
        self._type = frontDirection
        self.groups = []

    def move(self):
        if self.currentWaitToMove:
            self.currentWaitToMove -= 1

        for group in self.groups:
            group.move()

    def getType(self):
        return self._type

    def addGroup(self, group):
        self.groups.append(group)

    def archersFire(self, target):
        if self.inDefence:
            bonus = self.location.getArcheryBonusDefender()
        else:
            bonus = self.location.getArcheryBonusAttacker()

        for group in self.groups:
            group.archersFire(target, bonus)

    def meleeFire(self):
        if not self.currentFrontTarget and self.currentWaitToMove != 0:
            return

        targetFront = self.getTarget()

        if targetFront.getMeleeCount():
            generator = targetFront.getMeleeGroup()
        elif targetFront.getRangeCount():
            generator = targetFront.getRangeGroup()
        else:
            return False

        for group in self.groups:
            if not group.getTarget():
                targetGroup = next(generator)
                group.setTarget(targetGroup)

        for group in self.groups:
            group.meleeAttack()


    def getMeleeGroup(self, ignoreWithTarget=True):
        for group in self.groups:
            if group.getUnitsCount() and group.getMeleeCount():
                if ignoreWithTarget is True and not group.getTarget():
                    yield group
                elif ignoreWithTarget is False:
                    yield group

    def getRangeGroup(self, ignoreWithTarget=True):
        for group in self.groups:
            if group.getUnitsCount() and group.getRangeCount():
                if ignoreWithTarget is True and not group.getTarget():
                    yield group
                elif ignoreWithTarget is False:
                    yield group

    def getUnitsCount(self):
        frontSize = 0
        for group in self.groups:
            frontSize += group.getCount()

        return frontSize

    def getMeleeCount(self):
        frontSize = 0
        for group in self.groups:
            frontSize += group.getMeleeCount()

        return frontSize

    def getRangeCount(self):
        frontSize = 0
        for group in self.groups:
            frontSize += group.getRangeCount()

        return frontSize

    def isBussy(self):
        """Is this front in local battle"""
        return self.currentFrontTarget and self.currentWaitToMove != 0

    def getRandomGroup(self):
        """
        used by enemy
        :rtype: battle.structure.group.Group
        """
        return self.groups[ rand.randint(0, len(self.groups) - 1) ]

    def setLocation(self, location):
        """
        :type location: battle.places.abstract.AbstractPlace
        """
        self.location = location

    def setInDefence(self, inDefence):
        self.inDefence = inDefence

    def getTarget(self):
        """
        :rtype: Front
        """
        return self.currentFrontTarget

    def setTarget(self, targetFront, isClose=False):
        self.currentFrontTarget = targetFront
        self.setGroupsTargets(targetFront)

        if isClose:
            self.currentWaitToMove = 0
        else:
            self.currentWaitToMove = self.location.timeToAttack()

    def setGroupsTargets(self, targetFront):
        pass
