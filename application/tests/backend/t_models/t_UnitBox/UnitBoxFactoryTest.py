from tests.backend.t_models.t_UnitBox import generic

import models.UnitBox

class Backend_Models_UnitBox_UnitBoxFactoryTest(generic.Backend_Models_UnitBox_Generic):
    def testCreateUnit(self):
        domain = models.UnitBox.UnitBoxDomain.UnitBoxDomain()
        editDomain = domain.edit()

        editDomain.setUser(self.user)
        editDomain.setIsGeneral(True)
        editDomain.setSoliderCount(5000)
        editDomain.setHealth(500)
        editDomain.setAgility(500)
        editDomain.setAbsorption(500)
        editDomain.setStamina(400)

        editDomain.setHorseLevel(20)

        editDomain.setArmorType(domain.ARMOR_LEATHER)
        editDomain.setArmorLevel(10)

        editDomain.setWeaponType(domain.WEAPON_BOW)
        editDomain.setWeaponLevel(10)

        editDomain.setUseSecondWeapon(True)
        editDomain.setSecondWeaponType(domain.WEAPON_BLUNT)
        editDomain.setSecondWeaponLevel(10)

        editDomain.setRubins(500)
        editDomain.setStone(500)
        editDomain.setSteel(500)
        editDomain.setWood(500)
        editDomain.setEat(500)
        editDomain.setTime(10)

        editDomain.getFactory().add(editDomain)

        self.fullCleanCache()

        domain = models.UnitBox.Factory.factory.getById(domain.getId())

        self.assertEqual(domain.getUser().getId(), self.user.getId())
        self.assertEqual(domain.isGeneral(), True)
        self.assertEqual(domain.getSoliderCount(), 5000)
        self.assertEqual(domain.getHealth(), 500)
        self.assertEqual(domain.getAgility(), 500)
        self.assertEqual(domain.getAbsorption(), 500)
        self.assertEqual(domain.getStamina(), 400)

        self.assertEqual(domain.getHorseLevel(), 20)

        self.assertEqual(domain.getArmor(), {'type': domain.ARMOR_LEATHER, 'level': 10})
        self.assertEqual(domain.getWeapon(), {'type': domain.WEAPON_BOW, 'level': 10})
        self.assertEqual(domain.getSecondWeapon(), {
            'use': True,
            'type': domain.WEAPON_BLUNT,
            'level': 10
        })
