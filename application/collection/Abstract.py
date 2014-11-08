

class AbstractCollection(list):
    def __init__(self, *args):
        super().__init__(*args)
        self._loaded = False

    def getById(self, itemId):
        for i in self:
            if self[i].hasId() and self[i].getId() == itemId:
                return self[i]

    def extract(self, force=False):
        if len(self) == 0:
            return False

        mapper = self[0].getMapper()

        if not self._loaded or force:
            ids = []

            for i in self:
                if not i.hasId():
                    continue

                ids.append(i.getId())

            result = mapper.getByIds(ids)

            for i in result:
                domain = self.getById(i['_id'])
                domain.setOptions(i)

        return self
