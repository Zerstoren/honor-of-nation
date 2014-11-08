import service.User

class Decorate():
    def packDomainToJson(self, domain):
        user = domain.getUser()
        town = domain.getTown()

        if user:
            userId = service.User.Service_User().decorate('JsonPack').getUserDomain(
                user.getId()
            )
        else:
            userId = None

        if town:
            townId = str(town.getId())
        else:
            townId = None

        return {
            '_id': str(domain.getId()),
            'pos_id': domain.getPosId(),
            'type': domain.getType(),
            'user': userId,
            'town': townId,
            'amount': domain.getAmount(),
            'base_output': domain.getBaseOutput(),
            'output': domain.getOutput()
        }

    def getResourceByPosition(self, mapCoordinate, user=None):
        resource = super().getResourceByPosition(mapCoordinate, user)

        if resource is False:
            return False

        return self.packDomainToJson(resource)


