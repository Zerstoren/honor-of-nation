from . import abstract

class Dom(abstract.AbstractDeclaration):
    def selectOptionText(self, element, optionText):
        element.byXPath('//option[.="' + optionText + '"]').click()

    def selectOptionValue(self, element, optionValue):
        element.byXPath('//option[@value="' + optionValue + '"]').click()

    def value(self, element, value):
        element.clear()
        self.sleep(0.6)
        assert element.get_attribute('value') == "" or element.get_attribute('value') == "0"
        element.send_keys(str(value))
        assert element.get_attribute('value') == str(value)
