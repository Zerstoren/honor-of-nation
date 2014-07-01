from tests.backend.t_models.t_ArmorBox import generic
import models.ArmorBox


class Backend_Models_ArmorBox_ArmorBoxFactory(generic.Backend_Models_ArmorBox_Generic):
    def testCreateArmor(self):
        domain = models.ArmorBox.ArmorBoxDomain.ArmorBoxDomain()
        editDomain = domain.edit()

        editDomain.setUser(self.user)

        editDomain.setArmorType(domain.ARMOR_MAIL)
        editDomain.setUseShield(True)
        editDomain.setUseHorse(True)

        editDomain.setAgility(500)
        editDomain.setAbsorption(400)
        editDomain.setHealth(5000)
        editDomain.setLevel(20)

        editDomain.setShieldType(domain.SHIELD_STEEL)
        editDomain.setShieldDurability(400)
        editDomain.setShieldBlock(50)

        editDomain.setHorseHealth(3000)
        editDomain.setHorseSlope(50)
        editDomain.setHorseLevel(20)

        editDomain.setRubins(500)
        editDomain.setStone(500)
        editDomain.setSteel(500)
        editDomain.setWood(500)
        editDomain.setEat(500)
        editDomain.setTime(10)

        editDomain.getFactory().add(editDomain)

        self.fullCleanCache()

        domain = models.ArmorBox.Factory.factory.getById(domain.getId())
        self.assertEqual(domain.getUser().getId(), self.user.getId())
        self.assertEqual(domain.getAgility(), 500)
        self.assertEqual(domain.getAbsorption(), 400)
        self.assertEqual(domain.getHealth(), 5000)
        self.assertEqual(domain.getLevel(), 20)

        self.assertTrue(domain.isShieldUse())
        self.assertEqual(domain.getShieldType(), domain.SHIELD_STEEL)
        self.assertEqual(domain.getShieldDurability(), 400)
        self.assertEqual(domain.getShieldBlock(), 50)

        self.assertTrue(domain.isHorseUse())
        self.assertEqual(domain.getHorseSlope(), 50)
        self.assertEqual(domain.getHorseHealth(), 3000)
        self.assertEqual(domain.getHorseLevel(), 20)
