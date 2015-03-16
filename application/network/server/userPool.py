
class UserPool_Instance():
    users = {}

    def addUser(self, socket, userId):
        self.users[userId] = socket

    def removeUser(self, userId):
        del self.users[userId]

    def getUser(self, userId):
        return self.users[userId]

UserPool = UserPool_Instance()
