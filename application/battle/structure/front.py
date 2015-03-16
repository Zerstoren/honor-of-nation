

class Front(object):
    TYPE_AVANGARD = 0
    TYPE_LEFT_FLANG = 1
    TYPE_RIGHT_FLANG = 2
    TYPE_REAR = 4

    def __init__(self, frontDirection):
        self._type = frontDirection


