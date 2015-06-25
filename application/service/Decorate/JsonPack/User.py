
class Decorate():
    def packDomainToDict(self, domain):
        """
        :type domain: models.User.Domain.User_Domain
        """
        return {
            '_id': str(domain.getId()),
            'login': domain.getLogin(),
            'position': domain.getPosition()
        }

    def packUserStateToDict(self, domain):
        return {
            'user': str(domain.getTo().getId()),
            'state': domain.getState()
        }

    def login(self, login, password):
        result, domain = super().login(login, password)

        if domain:
            domain = self.packDomainToDict(domain)

        return (result, domain, )

    def getAllUsers(self):
        collection = super().getAllUsers()

        result = []
        for i in collection:
            result.append({
                '_id': str(i.getId()),
                'login': i.getLogin()
            })

        return result

    def getUserDomain(self, userId):
        return self.packDomainToDict(
            super().getUserDomain(userId)
        )

    def getUserStates(self, user):
        result = []
        collection = super().getUserStates(user)

        for item in collection:
            result.append(
                self.packUserStateToDict(item)
            )

        return result

    def getUserState(self, userFrom, userTo):
        return self.packDomainToDict(
            super().getUserStates(userFrom, userTo)
        )