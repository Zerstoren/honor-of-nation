from tests.backend.t_models.t_TownsBuilds import generic

import models.Towns.Factory

import time


class Backend_Models_TownsBuilds_TownsBuildDomainTest(generic.Backend_Models_TownsBuilds_Generic):
    def setUp(self):
        super().setUp()

        self.user = self.fixture.getUser(0)
        self.town = self._createTown(
            self._fillMapOneItem(40, 40),
            self.user
        )

    def testGetDomain(self):
        builds = self.town.getSubDomainBuilds()

        self.assertEqual(builds.getTown(), self.town)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_FIELD), 0)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_FARM), 0)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_MILL), 0)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_MINE), 0)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_ROAD), 0)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_V_COUNCIL), 0)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_HUT), 0)

    def testQueuePut(self):
        builds = self.town.getSubDomainBuilds()

        self.assertEqual(builds.getBuildLevel(builds.BUILD_FARM), 0)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_FIELD), 0)

        editBuilds = builds.edit()
        editBuilds.putBuildQueue(builds.BUILD_FARM, 1, 1)
        editBuilds.putBuildQueue(builds.BUILD_FARM, 2, 1)
        editBuilds.putBuildQueue(builds.BUILD_FIELD, 1, 1)
        editBuilds.getMapper().saveQueue(editBuilds)

        time.sleep(3)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_FARM), 2)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_FIELD), 1)

    def testQueueRemove(self):
        builds = self.town.getSubDomainBuilds()

        self.assertEqual(builds.getBuildLevel(builds.BUILD_FARM), 0)

        editBuilds = builds.edit()
        editBuilds.putBuildQueue(builds.BUILD_FARM, 1, 5)
        editBuilds.putBuildQueue(builds.BUILD_FARM, 2, 1)
        editBuilds.putBuildQueue(builds.BUILD_FARM, 3, 1)
        editBuilds.putBuildQueue(builds.BUILD_FARM, 4, 1)
        editBuilds.putBuildQueue(builds.BUILD_FIELD, 1, 1)
        editBuilds.getMapper().saveQueue(editBuilds)

        time.sleep(1)

        editBuilds = builds.edit()
        editBuilds.removeBuildQueue(builds.BUILD_FARM, 1)
        editBuilds.getMapper().saveQueue(editBuilds)

        time.sleep(1)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_FARM), 0)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_FIELD), 1)

    def testQueueClearCache(self):
        builds = self.town.getSubDomainBuilds()

        editBuilds = builds.edit()
        editBuilds.putBuildQueue(builds.BUILD_FARM, 1, 1)
        editBuilds.putBuildQueue(builds.BUILD_FARM, 2, 1)
        editBuilds.getMapper().saveQueue(editBuilds)

        del builds
        del editBuilds

        self.fullCleanCache()

        time.sleep(2)
        builds = self.town.getSubDomainBuilds()

        self.assertEqual(builds.getBuildLevel(builds.BUILD_FARM), 2)

    def testQueueDuplicateEntry(self):
        builds = self.town.getSubDomainBuilds()

        editBuilds = builds.edit()
        editBuilds.putBuildQueue(builds.BUILD_FARM, 1, 1)
        editBuilds.putBuildQueue(builds.BUILD_FARM, 1, 1)
        editBuilds.getMapper().saveQueue(editBuilds)

        self.assertEqual(
            len(builds.getQueue()),
            1
        )

    def testFirstQueueItemSaveTime(self):
        builds = self.town.getSubDomainBuilds()

        self.assertEqual(builds.getBuildLevel(builds.BUILD_FARM), 0)

        editBuilds = builds.edit()
        editBuilds.putBuildQueue(builds.BUILD_FARM, 1, 5)
        editBuilds.putBuildQueue(builds.BUILD_FARM, 2, 1)
        editBuilds.putBuildQueue(builds.BUILD_FARM, 3, 1)
        editBuilds.putBuildQueue(builds.BUILD_FARM, 4, 1)
        editBuilds.putBuildQueue(builds.BUILD_FIELD, 1, 1)
        editBuilds.getMapper().saveQueue(editBuilds)

        completeConstruct = builds.getQueue()[0]['complete_construct']

        editBuilds = builds.edit()
        editBuilds.removeBuildQueue(builds.BUILD_FARM, 2)
        editBuilds.getMapper().saveQueue(editBuilds)

        self.assertEqual(
            builds.getQueue()[0]['complete_construct'],
            completeConstruct
        )

    def testPutQueueAfterCompleteConstruct(self):
        """
        Ошибка заключается в том что, если здание закончило строиться, то добавив новое
         в очередь, построеное из очереди убрано не будет
        """
        builds = self.town.getSubDomainBuilds()

        editBuilds = builds.edit()
        editBuilds.putBuildQueue(builds.BUILD_FARM, 1, 1)
        editBuilds.putBuildQueue(builds.BUILD_FARM, 2, 1)
        editBuilds.getMapper().saveQueue(editBuilds)

        time.sleep(2)

        editBuilds = builds.edit()
        editBuilds.putBuildQueue(builds.BUILD_FARM, 3, 1)
        editBuilds.getMapper().saveQueue(editBuilds)

        self.assertEqual(len(builds.getQueue()), 1)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_FARM), 2)

        self.fullCleanCache()
        townDomain = models.Towns.Factory.factory.getById(self.town.getId())
        self.assertEqual(len(townDomain.getSubDomainBuilds().getQueue()), 1)
        self.assertEqual(builds.getBuildLevel(builds.BUILD_FARM), 2)
