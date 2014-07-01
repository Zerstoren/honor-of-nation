
class Decorate():
    def packDomainToDict(self, domain):
        """
        :type domain: models.User.Domain.User_Domain
        """
        result = domain.toDict()
        del result['password']

        return result


    def login(self, login, password):
        result, domain = super().login(login, password)

        if domain:
            domain = self.packDomainToDict(domain)

        return (result, domain, )
