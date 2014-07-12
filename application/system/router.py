import importlib
import config

routers = config.getRoutes()


def searchExecControllerMethod(path):
    try:
        fileName, actionClass, actionMethod = routers[path].split('.')
        module = importlib.import_module('controller.' + fileName + 'Controller')

        try:
            controllerClass = module.__getattribute__(actionClass + 'Controller')()
        except AttributeError:
            print("No class", actionClass)
            return False

        try:
            controllerMethod = controllerClass.__getattribute__(actionMethod)
        except AttributeError:
            print("No method", actionMethod)
            return False

        return controllerMethod

    except KeyError as e:
        print("Wrong Path", str(e))
        return False
