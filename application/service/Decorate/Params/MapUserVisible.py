
class Decorate():
    def getByChunks(self, user, chunks):
        return super().getByChunks(
            user,
            [int(i) for i in chunks]
        )

    def getByIds(self, user, ids):
        return super().getByIds(
            user,
            [int(i) for i in ids]
        )