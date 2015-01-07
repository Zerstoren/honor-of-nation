import importlib

class Service_Abstract(object):
    ACL = 'Acl'
    PARAMS = 'Params'
    JSONPACK = 'JsonPack'

    JSONPACK_ACL = ['JsonPack', 'Acl']
    PARAMS_ACL = ['Params', 'Acl']
    PARAMS_JSONPACK = ['Params', 'JsonPack']
    PARAMS_JSONPACK_ACL = ['Params', 'JsonPack', 'Acl']

    def decorate(self, *args):
        currentClassName = self.__class__.__name__
        classPrefixes = currentClassName.split('_')[-1]
        classList = [self.__class__]

        newClassName = 'Service_' + classPrefixes + '_Decorated'

        if len(args) and type(args[0]) is list:
            args = args[0]

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
