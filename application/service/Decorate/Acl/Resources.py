
class Decorate():
    def getResources(self, transferUser, userDomain):
        resources = super().getResources(transferUser, userDomain)

        if userDomain.getId() == transferUser.getId():
            return resources
        else:
            return {}
