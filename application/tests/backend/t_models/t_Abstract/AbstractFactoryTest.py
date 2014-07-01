from tests.backend.t_models.t_Abstract import generic
import tests.mock.Factory


class Backend_Models_Abstract_AbstractFactoryTest(generic.Backend_Models_Abstract_Generic):
    def testIndexClean(self):
        absDomain = tests.mock.Factory.MockFactory()
        absDomain.createRandom()
        cache = absDomain.createRandom()

        self.assertEqual(len(absDomain._FactoryIndexes__indexes['c']), 2)
        absDomain.GC()
        self.assertEqual(len(absDomain._FactoryIndexes__indexes['c']), 1)
