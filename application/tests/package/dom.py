from . import abstract

class Dom(abstract.AbstractDeclaration):
    def selectOptionText(self, element, optionText):
        element.byXPath('//option[.="' + optionText + '"]').click()

    def selectOptionValue(self, element, optionValue):
        element.byXPath('//option[@value="' + optionValue + '"]').click()
