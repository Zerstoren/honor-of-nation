from . import abstractGeneric
import hashlib
import random

class Generic(abstractGeneric.Abstract_Generic):
    def getRandomName(self, prefix='', length=8):
        return prefix + hashlib.md5(str(random.randint(0, 100000000)).encode()).hexdigest()[0:length]

    def getRandomInt(self, minimal=0, maximal=100, prefix=''):
        return prefix + str(random.randint(minimal, maximal)) if prefix else random.randint(minimal, maximal)

    def setUserAsAdmin(self, user):
        """
        :type user: models.User.Domain.User_Domain
        """
        user.setAdmin(True)
        user.getMapper().save(user)