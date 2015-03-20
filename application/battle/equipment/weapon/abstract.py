class AbstractWeapon(object):
    instance = None
    weaponType = None

    def getType(self):
        return self.weaponType

    def getModificationByArmor(self, armor):
        modification = self._getModification(armor.getType())
        return (100 + modification) / 100

    def _getModification(self, armorType):
        raise Exception("Not overridden method")

    @staticmethod
    def getInstance():
        if AbstractWeapon.instance is None:
            AbstractWeapon.instance = AbstractWeapon()

        return AbstractWeapon.instance
