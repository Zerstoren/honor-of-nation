from tests.backend.t_services.generic import Backend_Services_Generic
import service.Admin

from models.Map import Mapper
from models.Map import Common

class Backend_Services_AdminTest(Backend_Services_Generic):
    def _getService(self):
        return service.Admin.Service_Admin()

    def testFillCoordinate(self):
        service = self._getService()
        result = service.fillCoordinate({
            'fromX': 0,
            'fromY': 0,
            'toX': 1,
            'toY': 1
        }, 1, 1)

        self.assertTrue(result)

        where = Common.Common_Filter()
        where.add('x', 1)
        where.add('y', 1)
        result = list(Mapper.Map_Mapper._select(where))

        del result[0]['_id']
        self.assertDictEqual({
            'land_type': 1,
            'remove': 0,
            'build_type': 0,
            'x': 1,
            'y': 1,
            'chunk': 1,
            'pos_id': 2001,
            'land': 1,
            'decor': 0,
            'build': 0
        }, result[0])

        where = Common.Common_Filter()
        where.add('x', 0)
        where.add('y', 0)
        result = list(Mapper.Map_Mapper._select(where))

        del result[0]['_id']
        self.assertDictEqual({
            'land_type': 1,
            'remove': 0,
            'build_type': 0,
            'x': 0,
            'y': 0,
            'chunk': 1,
            'pos_id': 0,
            'land': 1,
            'decor': 0,
            'build': 0
        }, result[0])

    def testFillChunk(self):
        service = self._getService()
        result = service.fillChunks([1], 1, 1)

        self.assertTrue(result)

        where = Common.Common_Filter()
        where.add('x', 1)
        where.add('y', 1)
        result = list(Mapper.Map_Mapper._select(where))

        del result[0]['_id']
        self.assertDictEqual({
            'land_type': 1,
            'remove': 0,
            'build_type': 0,
            'x': 1,
            'y': 1,
            'chunk': 1,
            'pos_id': 2001,
            'land': 1,
            'decor': 0,
            'build': 0
        }, result[0])

        where = Common.Common_Filter()
        where.add('x', 0)
        where.add('y', 0)
        result = list(Mapper.Map_Mapper._select(where))

        del result[0]['_id']
        self.assertDictEqual({
            'land_type': 1,
            'remove': 0,
            'build_type': 0,
            'x': 0,
            'y': 0,
            'chunk': 1,
            'pos_id': 0,
            'land': 1,
            'decor': 0,
            'build': 0
        }, result[0])
