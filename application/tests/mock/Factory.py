from models.abstract import Factory as AbsFactory
import libs.mongo
import random
import string


class MockFactory(AbsFactory.Factory):
    def __init__(self):
        import tests.mock.Domain
        import tests.mock.Mapper

        self.setIndexes('_id', 'a', 'b', 'c')

        self.Domain = tests.mock.Domain.MockDomain
        self.mapper = tests.mock.Mapper.MockMapper()

    def createRandom(self):
        domain = self.Domain()
        domainEdit = domain.edit()
        domainEdit.setId(self._getId())
        domainEdit.setA(random.choice(string.ascii_letters))
        domainEdit.setB(random.choice(string.ascii_letters))
        domainEdit.setC(random.randint(0, 999999))
        self.add(domainEdit)
        return domain

    def add(self, writer):
        self.mapper.add(writer)
        self.addDomainToIndex(writer.getDomain())

    def save(self, writer):
        self.snapDomainEditIndex(writer.getDomain())
        self.mapper.save(writer)
        self.applyDomainEditIndex(writer.getDomain())

    def _getId(self):
        return libs.mongo.types.ObjectId(
            ''.join(random.choice('0123456789') for x in range(24))
        )
