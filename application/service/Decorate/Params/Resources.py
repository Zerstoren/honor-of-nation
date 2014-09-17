
class Decorate():
    def setResources(self, user, resourcesData):
        for i in resourcesData:
            resourcesData[i] = int(resourcesData[i])

        return super().setResources(user, resourcesData)
