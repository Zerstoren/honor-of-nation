from service.Equipment.Weapon import Service_Equipment_Weapon
from service.Equipment.Armor import Service_Equipment_Armor
from service.Equipment.Units import Service_Equipment_Units

class Equipment(object):
    def createEquipmentWeapon(
        self,
        user,
        wType='sword',
        damage=100,
        speed=40,
        critical_chance=5,
        critical_damage=2
    ):
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

    def createEquipmentUnit(
        self,
        user,
        uType='solider',
        troopSize=0,
        health=300,
        agility=30,
        absorption=30,
        stamina=100,
        strength=20,
        armor=None,
        weapon=None,
        weaponSecond=None
    ):
        service = Service_Equipment_Units()

        if armor is None:
            armor = self.createEquipmentArmor(user)

        if weapon is None:
            weapon = self.createEquipmentWeapon(user)

        if weaponSecond is None:
            weaponSecond = False

        return service.save({
            'user': user.getId(),
            'type': uType,
            'troop_size':troopSize,
            'health': health,
            'agility': agility,
            'absorption': absorption,
            'stamina': stamina,
            'strength': strength,
            'armor': armor,
            'weapon': weapon,
            'weapon_second': weaponSecond
        })


    def getArmorByUser(self, user):
        return Service_Equipment_Armor().load(user)

    def getWeaponByUser(self, user):
        return Service_Equipment_Weapon().load(user)

    def getUnitByUser(self, user):
        return Service_Equipment_Units().load(user)
