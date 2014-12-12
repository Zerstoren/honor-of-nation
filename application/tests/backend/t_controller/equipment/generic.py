from tests.backend.t_controller.generic import Backend_Controller_Generic

from service.Equipment.Weapon import Service_Equipment_Weapon
from service.Equipment.Armor import Service_Equipment_Armor

class Backend_Controller_Equipment_Generic(Backend_Controller_Generic):

    def createEquipmentWeapon(self, user, wType='sword', damage=100, speed=40, critical_chance=5, critical_damage=2):
        service = Service_Equipment_Weapon()
        domain = service.save({
            'user': user.getId(),
            'type': wType,
            'damage': damage,
            'speed': speed,
            'critical_chance': critical_chance,
            'critical_damage': critical_damage
        }, user)

        return domain

    def createEquipmentArmor(
        self,
        user,
        aType='leather',
        health=30,
        agility=30,
        absorption=-10,
        shield=(False, 'wood', 150, 20,)
    ):
        service = Service_Equipment_Armor()

        shield, shieldType, shieldDurability, shieldBlocking = shield

        domain = service.save({
            'user': user.getId(),
            'type': aType,
            'health': health,
            'agility': agility,
            'absorption': absorption,
            'shield': shield,
            'shield_type': shieldType,
            'shield_durability': shieldDurability,
            'shield_blocking': shieldBlocking
        })

        return domain