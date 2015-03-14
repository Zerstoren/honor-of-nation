from tests.backend.t_controller.generic import Backend_Controller_Generic

import exceptions.resources

from service.TownBuilds import Service_TownBuilds

import time

import tests.rerun
from tests.package.db.town import Town


class Backend_Controller_TownBuildsTest(
    Backend_Controller_Generic,
    Town
):

    def _getTownBuildsController(self):
        import controller.TownBuildsController
        return controller.TownBuildsController.MainController()

    def _getCeleryController(self):
        import controller.TownBuildsController
        return controller.TownBuildsController.CeleryPrivateController()

    def setUp(self):
        self.initCelery()
        super().setUp()
        self.controller = self._getTownBuildsController()
        self.transfer = self._login()
        self.user = self.transfer.getUser()

        self.fillTerrain(0, 0, 2, 2)
        self.town = self.addTown(1, 1, self.user, 10000)
        self.builds = self.town.getBuilds()

        self.resources = self.user.getResources()
        self.resources.setRubins(1000000)
        self.resources.setWood(1000000)
        self.resources.setStone(1000000)
        self.resources.setSteel(1000000)
        self.resources.setEat(1000000)
        self.resources.getMapper().save(self.resources)

    def testCreateOneBuild(self):
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 1
        })

        self.assertTrue(
            self.transfer.getLastMessage()['message']['done']
        )

        build = self.town.getBuilds()
        build.extract(True)

        self.assertEqual(
            len(build.getQueue()),
            1
        )

        buildDataQueue = build.getQueue()[0]

        self.assertIsNotNone(buildDataQueue['queue_code'])
        self.assertEqual(buildDataQueue['key'], 'mill')
        self.assertEqual(buildDataQueue['level'], 1)
        self.assertEqual(buildDataQueue['complete_after'], 1)

    def testCreateNotEnoughResource(self):
        self.resources.setRubins(1)
        self.resources.getMapper().save(self.resources)

        self.assertRaises(
            exceptions.resources.NotEnoughResources,
            self.controller.createBuild,
            self.transfer,
            {
                'town': str(self.town.getId()),
                'key': 'mill',
                'level': 1
            }
        )

    def testCreateGroupBuild(self):
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 4
        })

        self.assertTrue(
            self.transfer.getLastMessage()['message']['done']
        )

        build = self.town.getBuilds()
        build.extract(True)

        self.assertEqual(
            len(build.getQueue()),
            4
        )

    def testCreateGroupBuildByLimit(self):
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 35
        })

        self.assertTrue(
            self.transfer.getLastMessage()['message']['done']
        )

        build = self.town.getBuilds()
        build.extract(True)

        self.assertEqual(
            len(build.getQueue()),
            10
        )

    def testCreateMixedBuild(self):
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 2
        })

        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'farm',
            'level': 1
        })

        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 3
        })

        build = self.town.getBuilds()
        build.extract(True)
        buildList = build.getQueue()

        self.assertEquals(
            len(buildList),
            4
        )

        self.assertEqual(buildList[0]['key'], 'mill')
        self.assertEqual(buildList[0]['level'], 1)

        self.assertEqual(buildList[1]['key'], 'mill')
        self.assertEqual(buildList[1]['level'], 2)

        self.assertEqual(buildList[2]['key'], 'farm')
        self.assertEqual(buildList[2]['level'], 1)

        self.assertEqual(buildList[3]['key'], 'mill')
        self.assertEqual(buildList[3]['level'], 3)

    def testCeleryControllerBuilds(self):
        controller = self._getCeleryController()
        serviceTownBuilds = Service_TownBuilds().decorate(Service_TownBuilds.PARAMS)

        serviceTownBuilds.create(
            self.user,
            str(self.town.getId()),
            'mill',
            2
        )

        time.sleep(1)

        townBuildsDomain = serviceTownBuilds.get(self.town, self.user)
        townQueueData = townBuildsDomain.getQueue()[0]
        townQueueData['town'] = str(self.town.getId())

        controller.buildComplete(townQueueData)

        townBuildsDomain.extract(True)

        self.assertEqual(townBuildsDomain.getMill(), 1)
        self.assertEqual(1, len(townBuildsDomain.getQueue()))
        self.assertIsNotNone(
            townBuildsDomain.getQueue()[0]['queue_code']
        )

    def testRemoveGroupBuild(self):
        buildsDomain = self.town.getBuilds()
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 5
        })

        self.controller.removeBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 0
        })

        buildsDomain.extract(True)
        self.assertEqual(
            len(buildsDomain.getQueue()),
            0
        )
        self.assertEqual(
            buildsDomain.getMill(),
            0
        )

    def testRemoveMixedBuild(self):
        buildsDomain = self.town.getBuilds()
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 1
        })

        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'farm',
            'level': 1
        })

        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 2
        })

        self.controller.removeBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 0
        })

        buildsDomain.extract(True)
        self.assertEqual(
            len(buildsDomain.getQueue()),
            1
        )
        self.assertEqual(
            buildsDomain.getMill(),
            0
        )


class Backend_Controller_TownBuildsCeleryTest(
    Backend_Controller_Generic,
    Town
):
    def _getTownBuildsController(self):
        import controller.TownBuildsController
        return controller.TownBuildsController.MainController()

    def _getCeleryController(self):
        import controller.TownBuildsController
        return controller.TownBuildsController.CeleryPrivateController()

    def _getCeleryController(self):
        import controller.TownBuildsController
        return controller.TownBuildsController.CeleryPrivateController()

    def setUp(self):
        self.initCelery()
        super().setUp()
        self.controller = self._getTownBuildsController()
        self.transfer = self._login()
        self.user = self.transfer.getUser()

        self.fillTerrain(0, 0, 2, 2)
        self.town = self.addTown(1, 1, self.user, 10000)
        self.builds = self.town.getBuilds()

        self.resources = self.user.getResources()
        self.resources.setRubins(1000000)
        self.resources.setWood(1000000)
        self.resources.setStone(1000000)
        self.resources.setSteel(1000000)
        self.resources.setEat(1000000)
        self.resources.getMapper().save(self.resources)


    @tests.rerun.retry()
    def testWaitCompleteQueueBuild(self):
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 2
        })

        time.sleep(5)

        builds = self.town.getBuilds()
        builds.extract(True)

        self.assertEqual(builds.getMill(), 2)

    @tests.rerun.retry()
    def testWaitCompleteMixedQueueBuilds(self):
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 1
        })
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'farm',
            'level': 1
        })
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 2
        })

        time.sleep(8)

        builds = self.town.getBuilds()
        builds.extract(True)

        self.assertEqual(builds.getMill(), 2)
        self.assertEqual(builds.getFarm(), 1)

    @tests.rerun.retry()
    def testRemoveOneBuildFromQueue(self):
        buildsDomain = self.town.getBuilds()

        self.assertEqual(
            self.resources.extract(True).toDict(),
            {'eat': 1000000, 'gold': 1000000, 'rubins': 1000000, 'stone': 1000000, 'steel': 1000000, 'wood': 1000000}
        )

        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 1
        })

        self.assertEqual(
            self.resources.extract(True).toDict(),
            {'eat': 1000000, 'gold': 1000000, 'rubins': 999910, 'stone': 999910, 'steel': 1000000, 'wood': 999955}
        )

        self.controller.removeBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 0
        })

        self.assertEqual(
            self.resources.extract(True).toDict(),
            {'eat': 1000000, 'gold': 1000000, 'rubins': 1000000, 'stone': 1000000, 'steel': 1000000, 'wood': 1000000}
        )

        buildsDomain.extract(True)
        self.assertEqual(
            len(buildsDomain.getQueue()),
            0
        )
        self.assertEqual(
            buildsDomain.getMill(),
            0
        )

    @tests.rerun.retry()
    def testWaitCompleteBuild(self):
        self.controller.createBuild(self.transfer, {
            'town': str(self.town.getId()),
            'key': 'mill',
            'level': 1
        })

        time.sleep(3)

        builds = self.town.getBuilds()
        builds.extract(True)

        self.assertEqual(builds.getMill(), 1)
