import copy

class Const(object):
    __dirlist = {}

    def __init__(self, **kwargs):
        for i in kwargs:
            object.__setattr__(self, i.upper(), kwargs[i])
            self.__dirlist[i.upper()] = kwargs[i]

    def export(self):
        return copy.deepcopy(self.__dirlist)

    def __str__(self):
        return "NoneString"

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, *wards):
        pass

    def __delattr__(self, *wards):
        pass

    def __dir__(self):
        return self.__dirlist
