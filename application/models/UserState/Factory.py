import models.Abstract.Factory

from . import Domain
from models.User.Domain import User_Domain

from collection.UserStateCollection import UserState_Collection


class UserState_Factory_Main(models.Abstract.Factory.Abstract_Factory):
    def getDomainFromData(self, data):
        fromUser = User_Domain()
        fromUser.setId(data['from'])

        toUser = User_Domain()
        toUser.setId(data['to'])

        domain = Domain.UserState_Domain()
        domain.setFrom(fromUser)
        domain.setTo(toUser)
        domain.setState(int(data['state']))

        return domain

    def getCollectionFromData(self, data):
        collection = UserState_Collection()
        for item in data:
            collection.append(
                self.getDomainFromData(item)
            )

        return collection

UserState_Factory = UserState_Factory_Main()
