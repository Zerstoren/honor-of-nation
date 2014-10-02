from tests.selenium.Admin import generic

class Selenium_Admin_TerrainTest(generic.Selenium_Admin_Generic):
    def testCreateTerrainByCoordinate(self):
        self.login()
        self._goToAdmin()

        self.byCssSelector('div.from .x').send_keys(1)
        self.byCssSelector('div.from .y').send_keys(1)

        self.byCssSelector('div.to .x').send_keys(1)
        self.byCssSelector('div.to .y').send_keys(1)

        self.byXPath('//span[@data-type="1"]/button').click()

        self.byCssSelector('.send').click()

        self.operationIsSuccess()

    def testCreateTerrainByChunks(self):
        self.login()
        self._goToAdmin()

        self.byAttribute('data-type', 'chunk').click()

        self.byCssSelector('.block-chunk .chunk').send_keys(1)
        self.byCssSelector('.sl-add-to-list').click()
        try:
            self.byAttribute('data-chunk', '1')
        except self.NoSuchElementException:
            self.fail('Chunk not added')

        self.byCssSelector('.chunk-position .x').send_keys(16)
        self.byCssSelector('.chunk-position .y').send_keys(0)
        self.byCssSelector('.sl-add-to-list').click()
        try:
            self.byAttribute('data-chunk', '2')
        except self.NoSuchElementException:
            self.fail('Chunk not added')


        self.byAttribute('data-chunk', '2').click()
        try:
            self.byAttribute('data-chunk', '2')
            self.fail('Chunk not deleted')
        except self.NoSuchElementException:
            pass

        self.byXPath('//span[@data-type="1"]/button').click()

        self.byCssSelector('.send').click()

        self.operationIsSuccess()
