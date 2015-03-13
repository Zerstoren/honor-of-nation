from . import abstract

class Dom(abstract.AbstractDeclaration):
    def selectOptionText(self, element, optionText):
        element.byXPath('//option[.="' + optionText + '"]').click()

    def selectOptionValue(self, element, optionValue):
        element.byXPath('//option[@value="' + optionValue + '"]').click()

    def selectRange(self, element, leftSize):
        self.executeCommand('arguments[0].valueAsNumber = %i;' % leftSize, element)

    def value(self, element, value):
        self.executeCommand('arguments[0].value = "";', element)
        element.send_keys(value)

    def setAttribute(self, element, key, value):
        self.executeCommand("arguments[0].setAttribute(arguments[1], arguments[2]);", element, key, value)