from . import abstract

class Interface(abstract.AbstractDeclaration):
    def operationIsSuccess(self):
        try:
            self.waitForElement('.alertify-log-success')
        except self.TimeoutException:
            self.fail('Operation is not success')

        try:
            self.byCssSelector('.alertify-log-error')
            self.fail('Operation success show error message')
        except self.NoSuchElementException:
            pass

    def operationIsFail(self):
        try:
            self.waitForElement('.alertify-log-error')
        except self.TimeoutException:
            self.fail('Operation is not failed')

        try:
            self.byCssSelector('.alertify-log-success')
            self.fail('Operation error show success message')
        except self.NoSuchElementException:
            pass

    def hideSuccessOperation(self):
        self.byCssSelector('.alertify-log-success').click()
        self.waitForElementHide('.alertify-log-success')

    def hideFailOperation(self):
        self.byCssSelector('.alertify-log-error').click()
        self.waitForElementHide('.alertify-log-error')

    def getResources(self, fromBlock='.mpi__header .resources'):
        resourceBlock = self.byCssSelector(fromBlock)
        return {
            "rubins": int(resourceBlock.byCss('.rubins').get_attribute('data-hint').replace(' ', '')),
            "steel": int(resourceBlock.byCss('.steel').get_attribute('data-hint').replace(' ', '')),
            "eat": int(resourceBlock.byCss('.eat').get_attribute('data-hint').replace(' ', '')),
            "stone": int(resourceBlock.byCss('.stone').get_attribute('data-hint').replace(' ', '')),
            "wood": int(resourceBlock.byCss('.wood').get_attribute('data-hint').replace(' ', '')),
            "gold": int(resourceBlock.byCss('.gold').get_attribute('data-hint').replace(' ', '')),
        }

    def openTown(self, town):
        self.goAppUrl('/town/' + str(town.getId()))
        self.waitForElement('#map-body-holder > .town .content')
