import importlib

class Service_Abstract(object):
    def decorate(self, *args):
        currentClassName = self.__class__.__name__
        classPrefixes = currentClassName.split('_')[-1]
        classList = [self.__class__]

        newClassName = 'Service_' + classPrefixes + '_Decorated'
        args = list(args)
        args.reverse()
        for arg in args:
            path = 'service.Decorate.' + arg + '.' + classPrefixes
            try:
                classList.append(
                    importlib.import_module(path).Decorate
                )

                newClassName += '_' + arg
            except AttributeError:
                raise ImportError('Not found class Decorated in %s' % path)

        classList.reverse()
        return type(newClassName, tuple(classList), {})()
