import exceptions.httpCodes

class Decorate(object):
    def get(self, _id, user=None):
        domain = super().get(_id, user)

        if domain.getUser().getId() != user.getId():
            raise exceptions.httpCodes.Page403("Cant access to weapon")

        return domain