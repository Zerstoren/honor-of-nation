from tests.unit.generic import UnitTest_Generic

from battle.simulate import rand
from battle.structure.unit import Unit

from battle.equipment.armor.mail import Mail as Armor_Mail
from battle.equipment.armor.leather import Leather as Armor_Leather
from battle.equipment.armor.plate import Plate as Armor_Plate

from battle.equipment.shield.wood import Wood as Shield_Wood
from battle.equipment.shield.steel import Steel as Shield_Steel

from battle.equipment.weapon.blunt import Blunt as Weapon_Blunt
from battle.equipment.weapon.bow import Bow as Weapon_Bow
from battle.equipment.weapon.spear import Spear as Weapon_Spear
from battle.equipment.weapon.sword import Sword as Weapon_Sword

from models.Equipment.Armor.Data import const as ArmorConst
from models.Equipment.Weapon.Data import const as WeaponConst

import importlib


class UnitTest_Battle_Generic(UnitTest_Generic):
    randomDisabled = False

    TYPE_WEAPON_SWORD = WeaponConst.SWORD
    TYPE_WEAPON_BLUNT = WeaponConst.BLUNT
    TYPE_WEAPON_SPEAR = WeaponConst.SPEAR
    TYPE_WEAPON_BOW = WeaponConst.BOW

    TYPE_ARMOR_LEATHER = ArmorConst.ARMOR_LEATHER
    TYPE_ARMOR_MAIL = ArmorConst.ARMOR_MAIL
    TYPE_ARMOR_PLATE = ArmorConst.ARMOR_PLATE

    TYPE_SHIELD_WOOD = ArmorConst.SHIELD_WOOD
    TYPE_SHIELD_STEEL = ArmorConst.SHIELD_STEEL

    def tearDown(self):
        super().tearDown()
        if self.randomDisabled:
            self.randomDisabled = False
            importlib.reload(rand)

    def disableRandomChoice(self, always=False):
        self.randomDisabled = True

        def choice(chance):
            return always

        rand.chance = choice

    def createUnit(
        self,
        weaponType='sword',
        armorType='leather',
        shieldType=None,
        secondWeaponType=None,

        health = 0,
        agility = 0,
        absorption = 0,
        strength = 0,
        stamina = 0,

        shieldDurability = 0,
        shieldBlocking = 0,

        damage = 0,
        attackSpeed = 0,
        criticalDamage = 0,
        criticalChance = 0,

        second_damage = 0,
        second_attackSpeed = 0,
        second_criticalDamage = 0,
        second_criticalChance = 0,

    ):
        unit = Unit(None)
        if weaponType == WeaponConst.SWORD: unit.weapon = Weapon_Sword.getInstance()
        elif weaponType == WeaponConst.BLUNT: unit.weapon = Weapon_Blunt.getInstance()
        elif weaponType == WeaponConst.SPEAR: unit.weapon = Weapon_Spear.getInstance()
        elif weaponType == WeaponConst.BOW: unit.weapon = Weapon_Bow.getInstance()

        if armorType == ArmorConst.ARMOR_LEATHER: unit.armor = Armor_Leather.getInstance()
        elif armorType == ArmorConst.ARMOR_MAIL: unit.armor = Armor_Mail.getInstance()
        elif armorType == ArmorConst.ARMOR_PLATE: unit.armor = Armor_Plate.getInstance()

        if shieldType == ArmorConst.SHIELD_WOOD: unit.shield = Shield_Wood.getInstance()
        elif shieldType == ArmorConst.SHIELD_STEEL: unit.shield = Shield_Steel.getInstance()

        if secondWeaponType == WeaponConst.SWORD: unit.second_weapon = Weapon_Sword.getInstance()
        elif secondWeaponType == WeaponConst.BLUNT: unit.second_weapon = Weapon_Blunt.getInstance()
        elif secondWeaponType == WeaponConst.SPEAR: unit.second_weapon = Weapon_Spear.getInstance()
        elif secondWeaponType == WeaponConst.BOW: unit.second_weapon = Weapon_Bow.getInstance()

        unit.health = health
        unit.agility = agility
        unit.absorption = absorption
        unit.strength = strength
        unit.stamina = stamina

        unit.shieldDurability = shieldDurability
        unit.shieldBlocking = shieldBlocking

        unit.damage = damage
        unit.attackSpeed = attackSpeed
        unit.criticalChance = criticalChance
        unit.criticalDamage = criticalDamage

        unit.second_damage = second_damage
        unit.second_attackSpeed = second_attackSpeed
        unit.second_criticalChance = second_criticalChance
        unit.second_criticalDamage = second_criticalDamage

        return unit