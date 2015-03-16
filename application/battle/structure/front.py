from battle.simulate import rand


class FrontCollection(object):
    avangard = None
    leftFlang = None
    rightFlang = None
    rear = None

    def __init__(self, inDefence):
        self.inDefence = inDefence

    def getArcheryTarget(self):
        """Used by enemy"""
        avangardSize = self.avangard.getUnitsCount()
        leftFlang = self.leftFlang.getUnitsCount()
        rightFlang = self.rightFlang.getUnitsCount()
        target = None

        if avangardSize >= 0:
            target = self.avangard

        if leftFlang >= avangardSize:
            target = self.leftFlang

        if rightFlang >= leftFlang:
            target = self.rightFlang

        return target

    def iterateAll(self):
        for i in [self.avangard, self.leftFlang, self.rightFlang, self.rear]:
            yield i

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
        self.avangard.setLocation(location)
        self.leftFlang.setLocation(location)
        self.rightFlang.setLocation(location)
        self.rear.setLocation(location)

class Front(object):
    TYPE_AVANGARD = 0
    TYPE_LEFT_FLANG = 1
    TYPE_RIGHT_FLANG = 2
    TYPE_REAR = 4

    TYPES = (1, 2, 3, 4, )

    location = None
    inDefence = None

    def __init__(self, frontDirection):
        self._type = frontDirection
        self.groups = []

    def addGroup(self, group):
        self.groups.append(group)

    def archersFire(self, target):
        if self.inDefence:
            bonus = self.location.getArcheryBonusDefender()
        else:
            bonus = self.location.getArcheryBonusAttacker()

        for group in self.groups:
            group.archerFire(target, bonus)

    def getUnitsCount(self):
        frontSize = 0
        for group in self.groups:
            frontSize += group.getCount()

        return frontSize

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