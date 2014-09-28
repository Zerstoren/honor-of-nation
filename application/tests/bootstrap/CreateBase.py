from models.User.Domain import User_Domain
from models.User.Factory import User_Factory
from models.Resources.Domain import Resources_Domain
import hashlib
import random

class CreateBase(object):
    def __init__(self):
        self.__User()

    def getRandomName(self, prefix='', length=8):
        return prefix + hashlib.md5(str(random.randint(0, 100000000)).encode()).hexdigest()[0:length]

    def getRandomInt(self, minimal=0, maximal=100, prefix=''):
        return prefix + str(random.randint(minimal, maximal)) if prefix else random.randint(minimal, maximal)

    def getUser(self, n):
        """
        :rtype: User_Domain
        """
        return self._user[n]

    def __User(self):
        self._user = []


        self._user.append(
            self._createUser('Zerst', '12345', admin=True)
        )

        for i in range(1, 4):
            self._user.append(
                self._createUser(self.getRandomName('Login_'), self.getRandomName('Password_'))
            )

    def _createUser(self, login, password, admin=False):
        domain = User_Domain()
        domain.setLogin(login)
        domain.setPassword(password)
        domain.setAdmin(admin)
        domain._domain_data['_testPassword'] = password
        domain.setPosition(1, 1)
        domain.getMapper().save(domain)

        User_Factory.setCache(domain.getId(), domain)

        resource = Resources_Domain()
        resource.setUser(domain)
        resource.setRubins(1000000)
        resource.setEat(1000000)
        resource.setWood(1000000)
        resource.setSteel(1000000)
        resource.setStone(1000000)
        resource.setGold(1000000)
        resource.getMapper().save(resource)

        return domain
