

class AbstractWeapon(object):
    instance = None

    @staticmethod
    def getInstance():
        if AbstractWeapon.instance is None:
            AbstractWeapon.instance = AbstractWeapon()

        return AbstractWeapon.instance
