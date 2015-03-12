from . import abstract

class Dom(abstract.AbstractDeclaration):
    def selectOptionText(self, element, optionText):
        element.byXPath('//option[.="' + optionText + '"]').click()

    def selectOptionValue(self, element, optionValue):
        element.byXPath('//option[@value="' + optionValue + '"]').click()

    def value(self, element, value):
        self.executeCommand('arguments[0].value = "";', element)
        element.send_keys(value)
        # chain = self.getChainAction()
        # chain.click(element)
        # chain.key_down(self.keys.LEFT_SHIFT)
        # chain.key_down(self.keys.HOME)
        # chain.key_up(self.keys.HOME)
        # chain.key_down(self.keys.BACKSPACE)
        # chain.key_up(self.keys.BACKSPACE)
        # chain.key_up(self.keys.LEFT_SHIFT)
        # chain.perform()
        #
        # element.send_keys(str(value))
        # counter = 0
        # while True:
        #     if counter == 100:
        #         raise Exception("Something is wrong with set values. Expected '%s' but have '%s'" % (
        #             str(value), element.get_attribute('value')
        #         ))
        #     try:
        #         assert element.get_attribute('value') == str(value)
        #         break
        #     except AssertionError:
        #         counter += 1
        #         self.sleep(0.2)


