from service.Abstract.AbstractEquipment import AbstractEquipment

from models.Equipment.Units.Factory import Equipment_Units_Factory

import models.Equipment.Units.Data as Data

from helpers import math


class Service_Equipment_Units(AbstractEquipment):
    def save(self, data, user=None):
        domain = self._getArmorCalculatedDomain(data)
        domain.setUser(data['user'])

        domain.getMapper().save(domain)

        return domain

    def simulate(self, data):
        return self._getArmorCalculatedDomain(data)

    def get(self, _id, user=None):
        return Equipment_Units_Factory.get(_id)

    def getForce(self, _id, user=None):
        return Equipment_Units_Factory.get(_id, force=True)

    def load(self, user):
        return Equipment_Units_Factory.load(user)

    def remove(self, _id, user=None):
        domain = Equipment_Units_Factory.get(_id)
        domain.getMapper().remove(domain)
        return True

    def _getArmorCalculatedDomain(self, data):
        data = self._fixLevels(data)

        domain = Equipment_Units_Factory.getDomainFromData(data)

        currentPrice = self._calculatePrice(domain)

        domain.setTime(currentPrice['time'])

        domain.setRubins(currentPrice['rubins'])
        domain.setWood(currentPrice['wood'])
        domain.setSteel(currentPrice['steel'])
        domain.setEat(currentPrice['eat'])

        self._addEquipmentToPrice(domain)

        return domain

    def _addEquipmentToPrice(self, domain):
        armor = domain.getArmor()
        weapon = domain.getWeapon()
        weaponSecond = domain.getWeaponSecond()

        resources = ['rubins', 'steel', 'wood', 'eat', 'time']

        for resource in resources:
            domain.set(
                resource,
                domain.get(resource) +
                    armor.get(resource) +
                    weapon.get(resource) +
                    (weaponSecond.get(resource) if weaponSecond else 0)
            )


    def _fixLevels(self, data):
        names = ['troop_size', 'health', 'agility', 'absorption', 'strength', 'stamina']

        for name in names:
            level = data[name]
            typeItem = name

            if level < Data.unit[typeItem]['min']:
                level = Data.unit[typeItem]['min']

            data[name] = level

        return data

    def _calculatePrice(self, domain):
        """
        :type domain: models.Equipment.Units.Domain.Equipment_Units_Domain
        """

        price = {
            'rubins': 0,
            'steel': 0,
            'wood': 0,
            'eat': 0,
            'time': 0
        }

        defaultPrice = {
            'rubins': 0,
            'steel': 0,
            'wood': 0,
            'eat': 0,
            'time': 0
        }

        for priceKey in price:
            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getHealth(), 'health'),
                Data.unit['health'][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getAgility(), 'agility'),
                Data.unit['agility'][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getAbsorption(), 'absorption'),
                Data.unit['absorption'][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getStamina(), 'stamina'),
                Data.unit['stamina'][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getStrength(), 'strength'),
                Data.unit['strength'][priceKey]
            )

            price[priceKey] += self._linearCalc(
                domain.getTroopSize(),
                Data.unit['troop_size'][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                domain.getArmor().getLevel(),
                Data.unit['armor'][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                domain.getWeapon().getLevel(),
                Data.unit['weapon'][priceKey]
            )

            if domain.getWeaponSecond():
                price[priceKey] += self._exponentCalc(
                    domain.getWeaponSecond().getLevel(),
                    Data.unit['weapon_second'][priceKey]
                )

            if price[priceKey] < defaultPrice[priceKey]:
                price[priceKey] = defaultPrice[priceKey]

            price[priceKey] = math.rate(int(price[priceKey]))

        return price

    def _normalizeLevel(self, level, typeItem):
        if level < Data.unit[typeItem]['min']:
            level = Data.unit[typeItem]['min']

        return level - Data.unit[typeItem]['base']

    def _getDefaultPrice(self, shield):
        return {
            'rubins': 3000,
            'eat': 500,
            'steel': 150,
            'wood': 2000,
            'time': 5
        }

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_Equipment_Units
        """
        return super().decorate(*args)
