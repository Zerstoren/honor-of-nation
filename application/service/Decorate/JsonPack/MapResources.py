
class Decorate():
    def packDomainToJson(self, domain):
        return {
            '_id': str(domain.getId()),
            'pos_id': domain.getPosId(),
            'type': domain.getType(),
            'user': domain.getUser(),
            'town': None,
            'count': domain.getCount(),
            'production': domain.getProduction()
        }

    def getResourceByPosition(self, x, y):
        resource = super().getResourceByPosition(x, y)
        if resource is False:
            return False

        return self.packDomainToJson(resource)


