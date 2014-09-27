from tests.selenium.Admin import generic

import service.MapResources

class Selenium_Admin_ResourcesTest(generic.Selenium_Admin_Generic):
    def _goToAdmin(self):
        self.login()
        super()._goToAdmin()
        self.byAttribute('data-type', 'resources').click()

    def testCreateResource(self):
        self.fillTerrain(0, 0, 2, 2)
        self._goToAdmin()

        self.byCssSelector('.create').click()

        self.byCssSelector('.resource-coordinate').clear()
        self.byCssSelector('.resource-coordinate').send_keys('1x1')
        self.selectOptionText(
            self.byCssSelector('.resource-type'),
            'Дрова'
        )

        self.byCssSelector('.count').send_keys(2500000)
        self.byCssSelector('.production').send_keys(2500)

        self.byCssSelector('.save').click()
        self.operationIsSuccess()

        resource = service.MapResources.Service_MapResources().getResourceByPosition(1, 1)

        self.assertEqual(resource.getType(), 'wood')
        self.assertEqual(resource.getAmount(), 2500000)
        self.assertEqual(resource.getBaseOutput(), 2500)

    def testEditResource(self):
        self.fillTerrain(0, 0, 2, 2)
        service.MapResources.Service_MapResources().saveResources({
            'amount': 500000,
            'base_output': 5000,
            'output': 5000,
            'posId': 2001,
            'town': None,
            'user': None,
            'type': 'steel'
        })

        self._goToAdmin()

        self.byCssSelector('.coordinate').send_keys('1x1')
        self.byXPath('//button[.="Искать"]').click()

        self.waitForElement('.resource-coordinate')

        self.byCssSelector('.count').clear()
        self.byCssSelector('.production').clear()

        self.selectOptionText(
            self.byCssSelector('.resource-type'),
            'Дрова'
        )
        self.byCssSelector('.count').send_keys(2500000)
        self.byCssSelector('.production').send_keys(2500)

        self.byCssSelector('.save').click()
        self.operationIsSuccess()

        resource = service.MapResources.Service_MapResources().getResourceByPosition(1, 1)

        self.assertEqual(resource.getType(), 'wood')
        self.assertEqual(resource.getAmount(), 2500000)
        self.assertEqual(resource.getBaseOutput(), 2500)