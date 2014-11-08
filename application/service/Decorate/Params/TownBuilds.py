import helpers.mongo
import models.Town.Factory
import models.User.Factory


class Decorate():
    def get(self, townDomain, user):
        return super().get(townDomain, user)

    def create(self, user, town, key, level):
        townDomain = models.Town.Factory.Town_Factory.getDomainById(
            helpers.mongo.objectId(town)
        )
        super().create(user, townDomain, key, level)

    def remove(self, user, town, key, level):
        townDomain = models.Town.Factory.Town_Factory.getDomainById(
            helpers.mongo.objectId(town)
        )

        super().remove(user, townDomain, key, level)
