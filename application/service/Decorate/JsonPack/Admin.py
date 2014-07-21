
class Decorate():
    def searchUser(self, userLogin, user):
        data = super().searchUser(userLogin, user)
        return {
            'login': data.getLogin(),
            'admin': data.getAdmin()
        },