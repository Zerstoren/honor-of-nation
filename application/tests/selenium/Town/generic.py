from tests.selenium import generic


class Selenium_Town_Generic(generic.Selenium_Generic):
    def loginToTown(self,  userDomain=None):
        self.login(userDomain)

        self.waitForSocket()
        self.moveToPath('town', {
            'townId': str(self.town.getId())
        })

        self.waitForSocket()

    def setUpDb(self, skipDb=False):
        super().setUpDb()

        self.user = self.fixture.getUser(0)
        resourcesUser = self.user.getSubDomainResource()
        editResourceUser = resourcesUser.edit()
        editResourceUser.setResource(resourcesUser.RESOURCE_EAT, 1000000)
        editResourceUser.setResource(resourcesUser.RESOURCE_RUBINS, 1000000)
        editResourceUser.setResource(resourcesUser.RESOURCE_STEEL, 1000000)
        editResourceUser.setResource(resourcesUser.RESOURCE_STONE, 1000000)
        editResourceUser.setResource(resourcesUser.RESOURCE_WOOD, 1000000)
        editResourceUser.getMapper().save(editResourceUser)

        mapDomain = self._fillMapOneItem(50, 50)
        mapDomain.addAccessToUser(self.user)

        self.town = self._createTown(
            mapDomain,
            self.user,
            0
        )
