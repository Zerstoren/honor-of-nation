import config
import re


def fromPositionToId(x, y):
    """
    Преобразовывает координаты XY в хранимую запись в БД

    @params integer x
    @params integer y
    @return integer - ID запись в БД
    """
    return int((y * int(config.get('map.size'))) + x)


def fromIdToPosition(posId):
    """
    "Преобразовывает хранимую запись с БД, в координту
    @params integer posId
    @return object {x,y}
    """

    sizeMap = int(config.get('map.size'))

    x = int(posId % sizeMap)
    y = int((posId - x) / sizeMap)
    return (x, y, )


def fromPositionToChank(x, y):
    """
    "Определяет чанк, в котором находится эта координата
    @params integer x
    @params integer y
    @return integer - Chank
    """
    chank = int(config.get('map.chank'))
    size = int(config.get('map.size'))

    return int(((y - y % chank) / chank * (size / chank)) + (x - x % chank) / chank + 1)


def fromChankToPosition(chank):
    chankSize = int(config.get('map.chank'))

    return (
        int(((chank % 125) - 1) * chankSize),
        int(chank / 125) * chankSize,
    )


def fromStringCoordinateToPositionId(coordinate):
    data = re.split(r'([0-9]{1,4})[^0-9]{1,}([0-9]{1,4})', coordinate)
    return fromPositionToId(int(data[1]), int(data[2]))


def aroundPosition(x, y, length):
    """
    Создает квадратную ячеек шириной length, отталкиваясь от позиции x y.
    Возвращает список ячеек
    """
    items = list()

    for yL in range(length * 2 + 1):
        localLengthY = yL - length
        for xL in range(length * 2 + 1):
            localLengthX = xL - length

            items.append((
                x - localLengthX,
                y - localLengthY,
            ))

    return items


def howFar(mapDomainSource, mapDomainTarget):
    """
    Возвращает, на сколько далеко два доменных объекта друг от друга
    @params mapDomainSource models.Map.MapDomain.MapDomain
    @params mapDomainTarget models.Map.MapDomain.MapDomain
    @returns integer
    """

    return max(
        abs(mapDomainSource.getPositionX() - mapDomainTarget.getPositionX()),
        abs(mapDomainSource.getPositionY() - mapDomainTarget.getPositionY()),
    )
