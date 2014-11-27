class Const(object):
    __dirlist = []

    def __init__(self, **kwargs):
        for i in kwargs:
            object.__setattr__(self, i.upper(), kwargs[i])
            self.__dirlist.append(i.upper())

    def __str__(self):
        return "NoneString"

    def __setattr__(self, *wards):
        pass

    def __delattr__(self, *wards):
        pass

    def __dir__(self):
        return self.__dirlist
