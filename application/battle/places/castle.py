from . import abstract


class Castle(abstract.AbstractPlace):
    instance = None

    @staticmethod
    def getInstance():
        if Castle.instance is None:
            Castle.instance = Castle()

        return Castle.instance
