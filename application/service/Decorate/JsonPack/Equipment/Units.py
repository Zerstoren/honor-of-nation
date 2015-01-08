from service.Equipment.Armor import Service_Equipment_Armor
from service.Equipment.Weapon import Service_Equipment_Weapon

class Decorate(object):
    def _pack(self, domain):
        serviceArmor = Service_Equipment_Armor().decorate(Service_Equipment_Armor.JSONPACK)
        serviceWeapon = Service_Equipment_Weapon().decorate(Service_Equipment_Weapon.JSONPACK)

        data = {
            'type': domain.getType(),

            'troop_size': domain.getTroopSize(),
            'health': domain.getHealth(),
            'agility': domain.getAgility(),
            'absorption': domain.getAbsorption(),
            'strength': domain.getStrength(),
            'stamina': domain.getStamina(),

            'armor': str(domain.getArmor().getId()),
            'weapon': str(domain.getWeapon().getId()),
            'weapon_second': str(domain.getWeaponSecond().getId()) if domain.getWeaponSecond() else False,

            'armor_data': serviceArmor.getForce(domain.getArmor().getId()),
            'weapon_data': serviceWeapon.getForce(domain.getWeapon().getId()),
            'weapon_second_data': serviceWeapon.getForce(domain.getWeaponSecond().getId()) if domain.getWeaponSecond() else False,

            'time': domain.getTime(),

            'rubins': domain.getRubins(),
            'wood': domain.getWood(),
            'steel': domain.getSteel(),
            'eat': domain.getEat()
        }

        if domain.hasId():
            data['_id'] = str(domain.getId())
            data['user'] = str(domain.getUser().getId())

        return data

    def simulate(self, data):
        domain = super().simulate(data)
        return self._pack(domain)

    def get(self, _id, user=None):
        domain = super().get(_id, user)
        return self._pack(domain)

    def getForce(self, _id, user=None):
        domain = super().getForce(_id, user)
        return self._pack(domain)

    def load(self, user):
        collection = super().load(user)
        result = []

        for domain in collection:
            result.append(self._pack(domain))

        return result

    def save(self, data, user=None):
        domain = super().save(data, user)
        return self._pack(domain)

    def remove(self, _id, user=None):
        return super().remove(_id, user)
