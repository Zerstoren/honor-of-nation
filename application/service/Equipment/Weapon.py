from application.service.Abstract.AbstractEquipment import AbstractEquipment

from models.Equipment.Weapon.Factory import Equipment_Weapon_Factory
from models.Equipment.Weapon.Domain import Equipment_Weapon_Domain
import models.Equipment.Weapon.Data as Data

from helpers import math


class Service_Equipment_Weapon(AbstractEquipment):
    def save(self, data, user=None):
        domain = self._getWeaponCalculatedDomain(data)
        domain.setUser(data['user'])

        domain.getMapper().save(domain)

        return domain

    def simulate(self, data):
        return self._getWeaponCalculatedDomain(data)

    def get(self, _id, user=None):
        return Equipment_Weapon_Factory.get(_id)

    def load(self, user):
        return Equipment_Weapon_Factory.load(user)

    def _getWeaponCalculatedDomain(self, data):
        domain = Equipment_Weapon_Domain()

        if '_id' in data:
            domain.setId(data['_id'])

        domain.setType(data['type'])
        domain.setDamage(data['damage'])
        domain.setSpeed(data['speed'])
        domain.setCriticalChance(data['critical_chance'])
        domain.setCriticalDamage(data['critical_damage'])

        currentPrice = self._calculatePrice(domain)

        domain.setLevel(currentPrice['level'])
        domain.setTime(currentPrice['time'])

        domain.setRubins(currentPrice['rubins'])
        domain.setWood(currentPrice['wood'])
        domain.setSteel(currentPrice['steel'])
        domain.setEat(currentPrice['eat'])

        return domain

    def _calculatePrice(self, domain):
        price = {
            'rubins': 0,
            'steel': 0,
            'wood': 0,
            'eat': 0,
            'time': 0,
            'level': 0.9999
        }

        defaultPrice = {
            'rubins': 0,
            'steel': 0,
            'wood': 0,
            'eat': 0,
            'time': 0,
            'level': 0.9999
        }

        weaponType = domain.getType()

        for priceKey in price:
            price[priceKey] += self._getDefaultPrice()[priceKey]
            defaultPrice[priceKey] += self._getDefaultPrice()[priceKey]

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getDamage(), weaponType, 'damage'),
                Data.weapon['damage'][weaponType][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getSpeed(), weaponType, 'speed'),
                Data.weapon['speed'][weaponType][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getCriticalChance(), weaponType, 'critical_chance'),
                Data.weapon['critical_chance'][weaponType][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getCriticalDamage(), weaponType, 'speed'),
                Data.weapon['critical_damage'][weaponType][priceKey]
            )


            if price[priceKey] < defaultPrice[priceKey]:
                price[priceKey] = defaultPrice[priceKey]

            price[priceKey] = math.rate(int(price[priceKey]))

        return price

    def _normalizeLevel(self, level, weaponType, typeItem):
        if level < Data.weapon[typeItem][weaponType]['min']:
            level = Data.weapon[typeItem][weaponType]['min']
        elif 'max' in Data.weapon[typeItem][weaponType]:
            if level > Data.weapon[typeItem][weaponType]['max']:
                level = Data.weapon[typeItem][weaponType]['max']


        return level - Data.weapon[typeItem][weaponType]['base']

    def _getDefaultPrice(self):
        return {
            'rubins': 3000,
            'eat': 500,
            'steel': 150,
            'wood': 2000,
            'time': 5,
            'level': 0
        }

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_Equipment_Weapon
        """
        return super().decorate(*args)
