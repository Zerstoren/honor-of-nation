

class AbstractPlace(object):
    @staticmethod
    def timeToAttack():
        """:rtype: int"""
        pass

    @staticmethod
    def getArcheryBonusDefender():
        """:rtype: int"""
        pass

    @staticmethod
    def getArcheryBonusAttacker():
        """:rtype: int"""
        pass

    @staticmethod
    def getSequenceOfStrategicActionsAttacker():
        """:rtype: object"""
        pass

    @staticmethod
    def getSequenceOfStrategicActionsDefender():
        """:rtype: object"""
        pass
