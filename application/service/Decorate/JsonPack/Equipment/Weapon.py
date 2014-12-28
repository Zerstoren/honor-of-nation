
class Decorate(object):
    def _pack(self, domain):
        data = {
            'type': domain.getType(),
            'damage': domain.getDamage(),
            'speed': domain.getSpeed(),
            'critical_chance': domain.getCriticalChance(),
            'critical_damage': domain.getCriticalDamage(),

            'level': domain.getLevel(),
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