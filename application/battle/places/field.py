from . import abstract


class Field(abstract.AbstractPlace):
    instance = None

    @staticmethod
    def getInstance():
        if Field.instance is None:
            Field.instance = Field()

        return Field.instance

