from service.User import Service_User


class Decorate():
    def openMapForUser(self, user, data, aclUser=None):
        user = Service_User().getUserDomain(user)
        return super().openMapForUser(user, data, aclUser)