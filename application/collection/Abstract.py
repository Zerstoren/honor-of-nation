import models.Abstract.Domain

class AbstractCollection(list):
    domain = None
    def __init__(self, *args):
        super().__init__(*args)
        self._loaded = False

    def filter(self, field, value):
        result = AbstractCollection()
        for item in self:
            if item.get(field) == value:
                result.append(item)

        return result

    def getById(self, itemId):
        for i in self:
            if i.hasId() and i.getId() == itemId:
                return i

    def setOptions(self, data):
        if self.domain is None:
            raise Exception("Domain not setup")

        for i in data:
            domain = self.domain(data=i)
            self.append(domain)

        return self

    def fillFromIdsList(self, ids):
        if self.domain is None:
            raise Exception("Domain not setup")

        self.clear()
        for i in range(len(ids)):
            self.append(self.domain(data={'_id': ids[i]}))

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
