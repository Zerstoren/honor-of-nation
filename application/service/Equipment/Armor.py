from service.Abstract.AbstractEquipment import AbstractEquipment

from models.Equipment.Armor.Factory import Equipment_Armor_Factory
from models.Equipment.Armor.Domain import Equipment_Armor_Domain
import models.Equipment.Armor.Data as Data

from helpers import math


class Service_Equipment_Armor(AbstractEquipment):
    def save(self, data, user=None):
        domain = self._getArmorCalculatedDomain(data)
        domain.setUser(data['user'])

        domain.getMapper().save(domain)

        return domain

    def simulate(self, data):
        return self._getArmorCalculatedDomain(data)

    def get(self, _id, user=None):
        return Equipment_Armor_Factory.get(_id)

    def getForce(self, _id, user=None):
        return Equipment_Armor_Factory.get(_id, force=True)

    def load(self, user):
        return Equipment_Armor_Factory.load(user)

    def remove(self, _id, user=None):
        domain = Equipment_Armor_Factory.get(_id)
        domain.getMapper().remove(domain)
        return True

    def _getArmorCalculatedDomain(self, data):
        data = self._fixLevels(data)
        domain = Equipment_Armor_Factory.getDomainFromData(data)

        currentPrice = self._calculatePrice(domain)

        domain.setLevel(currentPrice['level'])
        domain.setTime(currentPrice['time'])

        domain.setRubins(currentPrice['rubins'])
        domain.setWood(currentPrice['wood'])
        domain.setSteel(currentPrice['steel'])
        domain.setEat(currentPrice['eat'])

        return domain

    def _fixLevels(self, data):
        names = ['health', 'agility', 'absorption']
        armorType = data['type']

        for name in names:
            level = data[name]
            typeItem = name

            if level < Data.armor[typeItem][armorType]['min']:
                level = Data.armor[typeItem][armorType]['min']
            elif 'max' in Data.armor[typeItem][armorType]:
                if level > Data.armor[typeItem][armorType]['max']:
                    level = Data.armor[typeItem][armorType]['max']

            data[name] = level

        if 'shield' in data and data['shield']:
            names = ['shield_durability', 'shield_blocking']
            shieldType = data['shield_type']

            for name in names:
                level = data[name]
                typeItem = name

                if level < Data.armor[typeItem][shieldType]['min']:
                    level = Data.armor[typeItem][shieldType]['min']
                elif 'max' in Data.armor[typeItem][shieldType]:
                    if level > Data.armor[typeItem][shieldType]['max']:
                        level = Data.armor[typeItem][shieldType]['max']

                data[name] = level

        return data


    def _calculatePrice(self, domain):
        """
        :type domain: models.Equipment.Armor.Domain.Equipment_Armor_Domain
        """

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

        armorType = domain.getType()

        for priceKey in price:
            price[priceKey] += self._getDefaultPrice(
                domain.getShield()
            )[priceKey]
            defaultPrice[priceKey] += self._getDefaultPrice(
                domain.getShield()
            )[priceKey]

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getHealth(), armorType, 'health'),
                Data.armor['health'][armorType][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getAgility(), armorType, 'agility'),
                Data.armor['agility'][armorType][priceKey]
            )

            price[priceKey] += self._exponentCalc(
                self._normalizeLevel(domain.getAbsorption(), armorType, 'absorption'),
                Data.armor['absorption'][armorType][priceKey]
            )

            if domain.getShield():
                shieldType = domain.getShieldType()
                price[priceKey] += self._exponentCalc(
                    self._normalizeLevel(domain.getShieldDurability(), shieldType, 'shield_durability'),
                    Data.armor['shield_durability'][shieldType][priceKey]
                )

                price[priceKey] += self._exponentCalc(
                    self._normalizeLevel(domain.getShieldBlocking(), shieldType, 'shield_blocking'),
                    Data.armor['shield_blocking'][shieldType][priceKey]
                )

            if price[priceKey] < defaultPrice[priceKey]:
                price[priceKey] = defaultPrice[priceKey]

            price[priceKey] = math.rate(int(price[priceKey]))

        return price

    def _normalizeLevel(self, level, armorType, typeItem):
        if level < Data.armor[typeItem][armorType]['min']:
            level = Data.armor[typeItem][armorType]['min']
        elif 'max' in Data.armor[typeItem][armorType]:
            if level > Data.armor[typeItem][armorType]['max']:
                level = Data.armor[typeItem][armorType]['max']

        return level - Data.armor[typeItem][armorType]['base']

    def _getDefaultPrice(self, shield):
        return {
            'rubins': 3000 + (500 if shield else 0),
            'eat': 500 + (100 if shield else 0),
            'steel': 150 + (50 if shield else 0),
            'wood': 2000 + (50 if shield else 0),
            'time': 5 + (2 if shield else 0),
            'level': 0
        }

    def decorate(self, *args):
        """
        required for IDE static analyzer
        :rtype: Service_Equipment_Armor
        """
        return super().decorate(*args)
