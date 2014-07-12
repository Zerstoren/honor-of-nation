from tests.backend.t_models.t_Map import generic


class Backend_Models_Map_MapDomainTest(generic.Backend_Models_Map_Generic):
    def testDomainData(self):
        domain = self._createMapCell(40, 40)
        self.assertEqual(domain._getData(), {
            'y': 40,
            'x': 40,
            'land': 0,
            'land_type': 1,
            'decor': 0,
            'build': 0,
            'build_type': 0,
            'chunk': 253,
            'pos_id': 80040
        })

        self.assertEqual(domain.getId(), 80040)
        self.assertEqual(domain.getPositionX(), 40)
        self.assertEqual(domain.getPositionY(), 40)
        self.assertEqual(domain.getChunk(), 253)
        self.assertEqual(domain.getLand(), 0)
        self.assertEqual(domain.getLandType(), 1)

    def testDomainVisibleUserAdd(self):
        user = self.fixture.getUser(0)
        domain = self._createMapCell(40, 40)

        self.assertFalse(domain.isVisibleFor(user))

        domain.addAccessToUser(user)

        self.assertTrue(domain.isVisibleFor(user))

        # Error if raised
        domain.addAccessToUser(user)
