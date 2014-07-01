import readline
import time
import config
config.configType = 'test_server'

import system.mongo

localVars = {}


class MyCompleter(object):  # Custom completer

    def complete(self, text, state):
        self.options = sorted(globals().keys())

        if state == 0:
            if text.find('.') != -1:
                self.deepMethodVariable(text)

            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]

            else:
                self.matches = self.options[:]

        try:
            return self.matches[state]
        except IndexError:
            return None

    def deepMethodVariable(self, text):
        text = text.split('.')
        text = ".".join(text[0: -1])


        try:
            var = eval(text)
        except:
            return

        dirList = var.__dir__()

        for i in reversed(range(len(dirList))):
            value = dirList[i]
            if value[0:2] == '__':
                dirList.remove(value)
            else:
                dirList[i] = text + '.' + value
        self.options = sorted(list(dirList))

readline.set_completer(MyCompleter().complete)
readline.parse_and_bind('tab: complete')

while True:
    message = input()

    try:
        result = eval(message)
        if result: print(result)
    except Exception:
        try:
            exec(message)
        except Exception as e:
            print(str(e))
