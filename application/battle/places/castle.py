from . import abstract


class Castle(abstract.AbstractPlace):
    instance = None

    @staticmethod

    def getSequenceOfStrategicActionsAttacker():
        from battle.structure.front import Front
        return {
            Front.TYPE_AVANGARD: (
                Front.TYPE_AVANGARD,
                Front.TYPE_RIGHT_FLANG,
                Front.TYPE_LEFT_FLANG,
                Front.TYPE_REAR,
            ),

            Front.TYPE_LEFT_FLANG: (
                Front.TYPE_LEFT_FLANG,
                Front.TYPE_AVANGARD,
                Front.TYPE_RIGHT_FLANG,
                Front.TYPE_REAR,
            ),

            Front.TYPE_RIGHT_FLANG: (
                Front.TYPE_RIGHT_FLANG,
                Front.TYPE_LEFT_FLANG,
                Front.TYPE_AVANGARD,
                Front.TYPE_REAR
            )
        }

    @staticmethod
    def getSequenceOfStrategicActionsDefender():
        from battle.structure.front import Front
        return {
            Front.TYPE_AVANGARD: (),
            Front.TYPE_LEFT_FLANG: (),
            Front.TYPE_RIGHT_FLANG: (),
            Front.TYPE_REAR: ()
        }

    @staticmethod
    def getInstance():
        if Castle.instance is None:
            Castle.instance = Castle()

        return Castle.instance
