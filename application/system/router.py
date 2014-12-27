import importlib
import config
import system.log

routers = config.getRoutes()


def searchExecControllerMethod(path):
    try:
        fileName, actionClass, actionMethod = routers[path].split('.')
        module = importlib.import_module('controller.' + fileName + 'Controller')

        try:
            controllerClass = module.__getattribute__(actionClass + 'Controller')()
        except AttributeError:
            system.log.warn("No class %s" % actionClass)
            return False

        try:
            controllerMethod = controllerClass.__getattribute__(actionMethod)
        except AttributeError:
            system.log.warn("No method %s" % actionMethod)
            return False

        return controllerMethod

    except KeyError as e:
        system.log.warn("Wrong Path %s" % str(e))
        return False
