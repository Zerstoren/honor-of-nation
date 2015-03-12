from . import abstract

class Dom(abstract.AbstractDeclaration):
    def selectOptionText(self, element, optionText):
        element.byXPath('//option[.="' + optionText + '"]').click()

    def selectOptionValue(self, element, optionValue):
        element.byXPath('//option[@value="' + optionValue + '"]').click()

    def value(self, element, value):
        element.clear()
        counter = 0
        while True:
            if counter == 200:
                raise Exception("Something is wrong with clear values expected '' but have '%s'" % (
                    element.get_attribute('value')
                ))
            try:
                assert element.get_attribute('value') == "" or element.get_attribute('value') == "0"
                break
            except AssertionError:
                counter += 1
                self.sleep(0.2)


        element.send_keys(str(value))
        counter = 0
        while True:
            if counter == 100:
                raise Exception("Something is wrong with set values. Expected '%s' but have '%s'" % (
                    str(value), element.get_attribute('value')
                ))
            try:
                assert element.get_attribute('value') == str(value)
                break
            except AssertionError:
                counter += 1
                self.sleep(0.2)


