class Decorate():
    def packDomainToJson(self, domain):
        user = domain.getUser()

        if user:
            userId = str(user.getId())
        else:
            userId = None

        return {
            '_id': str(domain.getId()),
            'pos_id': domain.getPosId(),
            'type': domain.getType(),
            'user': userId,
            'town': None,
            'amount': domain.getAmount(),
            'base_output': domain.getBaseOutput()
        }

    def getResourceByPosition(self, mapCoordinate, user=None):
        resource = super().getResourceByPosition(mapCoordinate, user)

        if resource is False:
            return False

        return self.packDomainToJson(resource)


