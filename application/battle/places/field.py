from . import abstract


class Field(abstract.AbstractPlace):
    instance = None
    @staticmethod
    def timeToAttack():
        return 5

    @staticmethod
    def getArcheryBonusDefender():
        pass

    @staticmethod
    def getArcheryBonusAttacker():
        pass

    @staticmethod
    def getSequenceOfStrategicActionsAttacker():
        from battle.structure.front import Front
        return {
            Front.TYPE_AVANGARD: (
                Front.TYPE_RIGHT_FLANG,
                Front.TYPE_REAR,
                Front.TYPE_LEFT_FLANG,
            ),

            Front.TYPE_LEFT_FLANG: (
                Front.TYPE_REAR,
                Front.TYPE_RIGHT_FLANG,
                Front.TYPE_AVANGARD,
            ),

            Front.TYPE_RIGHT_FLANG: (
                Front.TYPE_REAR,
                Front.TYPE_LEFT_FLANG,
                Front.TYPE_AVANGARD
            ),

            Front.TYPE_REAR: (
                {
                    Front.TYPE_RIGHT_FLANG: (
                        Front.TYPE_RIGHT_FLANG,
                        Front.TYPE_LEFT_FLANG,
                        Front.TYPE_AVANGARD,
                        Front.TYPE_REAR
                    ),

                    Front.TYPE_LEFT_FLANG: (
                        Front.TYPE_LEFT_FLANG,
                        Front.TYPE_RIGHT_FLANG,
                        Front.TYPE_AVANGARD,
                        Front.TYPE_REAR
                    )
                }
            )
        }

    @staticmethod
    def getSequenceOfStrategicActionsDefender():
        return Field.getArcheryBonusAttacker()

    @staticmethod
    def getInstance():
        if Field.instance is None:
            Field.instance = Field()

        return Field.instance

