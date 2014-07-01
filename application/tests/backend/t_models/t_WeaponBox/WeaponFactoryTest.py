from tests.backend.t_models.t_WeaponBox import generic

import models.WeaponBox


class Backend_Models_WeaponBox_WeaponFactoryTest(generic.Backend_Models_WeaponBox_Generic):
    def testCreateWeapon(self):
        domain = models.WeaponBox.WeaponBoxDomain.WeaponBoxDomain()
        editDomain = domain.edit()

        editDomain.setUser(self.user)
        editDomain.setType(domain.TYPE_SPEAR)
        editDomain.setDamage(400)
        editDomain.setSpeed(50)
        editDomain.setCriticalDamage(1.5)
        editDomain.setCriticalChance(1.5)
        editDomain.setLevel(25)
        editDomain.setTime(25)
        editDomain.setRubins(25)
        editDomain.setEat(25)
        editDomain.setSteel(25)
        editDomain.setStone(25)
        editDomain.setWood(25)
        editDomain.getFactory().add(editDomain)

        self.fullCleanCache()

        domain = models.WeaponBox.Factory.factory.getById(domain.getId())

        self.assertEqual(domain.getUser().getId(), self.user.getId())
        self.assertEqual(domain.getType(), domain.TYPE_SPEAR)
        self.assertEqual(domain.getDamage(), 400)
        self.assertEqual(domain.getSpeed(), 50)
        self.assertEqual(domain.getCriticalChance(), 1.5)
        self.assertEqual(domain.getCriticalDamage(), 1.5)
        self.assertEqual(domain.getLevel(), 25)
        self.assertEqual(domain.getTime(), 25)
        self.assertEqual(domain.getPrice(), {
            'rubins': 25,
            'wood': 25,
            'stone': 25,
            'steel': 25,
            'eat': 25
        })

