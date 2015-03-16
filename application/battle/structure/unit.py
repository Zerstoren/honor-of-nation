import copy

from battle.equipment.armor.abstract import AbstractArmor
from battle.equipment.armor.mail import Mail as Armor_Mail
from battle.equipment.armor.leather import Leather as Armor_Leather
from battle.equipment.armor.plate import Plate as Armor_Plate

from battle.equipment.shield.abstract import AbstractShield
from battle.equipment.shield.wood import Wood as Shield_Wood
from battle.equipment.shield.steel import Steel as Shield_Steel

from battle.equipment.weapon.abstract import AbstractWeapon
from battle.equipment.weapon.blunt import Blunt as Weapon_Blunt
from battle.equipment.weapon.bow import Bow as Weapon_Bow
from battle.equipment.weapon.spear import Spear as Weapon_Spear
from battle.equipment.weapon.sword import Sword as Weapon_Sword

from models.Equipment.Armor.Data import const as ArmorConst
from models.Equipment.Weapon.Data import const as WeaponConst


class Unit(object):
    def __init__(self, armyInstance):
        self._id = None
        self.armor = AbstractArmor.getInstance()
        self.weapon = AbstractWeapon.getInstance()
        self.second_weapon = AbstractWeapon.getInstance()
        self.shield = AbstractShield.getInstance()

        self.steps = 0
        self.attackReady = True

        self.health = 0
        self.agility = 0
        self.absorption = 0
        self.strength = 0
        self.stamina = 0

        self.shieldDurability = 0
        self.shieldBlocking = 0

        self.damage = 0
        self.attackSpeed = 0
        self.criticalDamage = 0
        self.criticalChance = 0

        self.second_damage = 0
        self.second_attackSpeed = 0
        self.second_criticalDamage = 0
        self.second_criticalChance = 0

        if armyInstance:
            _parse(self, armyInstance)

    def cloneInstance(self):
        return copy.copy(self)


def _parse(self, armyInstance):
    """
    :type self: Unit
    :type armyInstance: models.Army.Domain.Army_Domain
    """
    self._id = str(armyInstance.getId())

    unitDomain = armyInstance.getUnit()
    armorDomain = unitDomain.getArmor()
    weaponDomain = unitDomain.getWeapon()
    weaponSecondDomain = unitDomain.getWeaponSecond()

    self.health += unitDomain.getHealth()
    self.agility += unitDomain.getAgility()
    self.stamina += unitDomain.getStamina()
    self.strength += unitDomain.getStrength()
    self.absorption += unitDomain.getAbsorption()

    self.health += armorDomain.getHealth()
    self.agility += armorDomain.getAgility()
    self.absorption += armorDomain.getAbsorption()

    armorType = armorDomain.getType()
    if armorType == ArmorConst.ARMOR_LEATHER: self.armor = Armor_Leather.getInstance()
    elif armorType == ArmorConst.ARMOR_MAIL: self.armor = Armor_Mail.getInstance()
    elif armorType == ArmorConst.ARMOR_PLATE: self.armor = Armor_Plate.getInstance()

    if armorDomain.getShield():
        self.shieldDurability = armorDomain.getShieldDurability()
        self.shieldBlocking = armorDomain.getShieldBlocking()

        shieldType = armorDomain.getShieldType()
        if shieldType == ArmorConst.SHIELD_WOOD: self.shield = Shield_Wood.getInstance()
        elif shieldType == ArmorConst.SHIELD_STEEL: self.shield = Shield_Steel.getInstance()

    self.damage = weaponDomain.getDamage()
    self.attackSpeed = weaponDomain.getSpeed()
    self.criticalDamage = weaponDomain.getCriticalDamage()
    self.criticalChance = weaponDomain.getCriticalChance()

    weaponType = weaponDomain.getType()
    if weaponType == WeaponConst.SWORD: self.weapon = Weapon_Sword.getInstance()
    elif weaponType == WeaponConst.BLUBT: self.weapon = Weapon_Blunt.getInstance()
    elif weaponType == WeaponConst.SPEAR: self.weapon = Weapon_Spear.getInstance()
    elif weaponType == WeaponConst.BOW: self.weapon = Weapon_Bow.getInstance()

    if weaponSecondDomain:
        self.second_damage = weaponSecondDomain.getDamage()
        self.second_attackSpeed = weaponSecondDomain.getSpeed()
        self.second_criticalDamage = weaponSecondDomain.getCriticalDamage()
        self.second_criticalChance = weaponSecondDomain.getCriticalChance()

        weaponType = weaponDomain.getType()
        if weaponType == WeaponConst.SWORD: self.second_weapon = Weapon_Sword.getInstance()
        elif weaponType == WeaponConst.BLUBT: self.second_weapon = Weapon_Blunt.getInstance()
        elif weaponType == WeaponConst.SPEAR: self.second_weapon = Weapon_Spear.getInstance()
        elif weaponType == WeaponConst.BOW: self.second_weapon = Weapon_Bow.getInstance()
