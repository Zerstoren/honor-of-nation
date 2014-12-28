import service.Equipment.Armor
import models.Equipment.Armor.Domain

class Equipment(object):
    def addArmor(
        self,
        user,
        aType='leather',
        health=100,
        absorption=100,
        agility=100,
        shield=False,
        shieldType='wood',
        shieldDurability=5000,
        shieldBlocking=80
    ):
        armorService = service.Equipment.Armor.Service_Equipment_Armor()
        return armorService.save(
            {
                'type': aType,
                'user': user,
                'health': health,
                'absorption': absorption,
                'agility': agility,
                'shield': shield,
                'shield_type': shieldType,
                'shield_durability': shieldDurability,
                'shield_blocking': shieldBlocking
            },
            user
        )


    def getArmorByUser(self, user):
        return service.Equipment.Armor.Service_Equipment_Armor().load(user)
