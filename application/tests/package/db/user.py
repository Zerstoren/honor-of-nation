class User(object):
    def setUserAsAdmin(self, user):
        """
        :type user: models.User.Domain.User_Domain
        """
        user.setAdmin(True)
        user.getMapper().save(user)
