from . import abstract
import lxml
import config

from models.Map.Factory import Map_Factory
from helpers.MapCoordinate import MapCoordinate


class Map(abstract.AbstractDeclaration):
    def mapCell(self, x, y):
        return MapCell(self, x, y)

    def moveCamera(self, fromPosition, toPosition):
        assert isinstance(fromPosition, MapCell)
        assert isinstance(toPosition, MapCell) or type(toPosition) is tuple

        actionChain = self.getChainAction()
        startX, startY = fromPosition.getPosition()
        completeX, completeY = toPosition if type(toPosition) is tuple else toPosition.getPosition()

        currentPosition = [startX, startY, ]

        if completeX - startX > 0:
            directionX = -1
        elif completeX - startX < 0:
            directionX = 1
        else:
            directionX = 0

        if completeY - startY > 0:
            directionY = -1
        elif completeY - startY < 0:
            directionY = 1
        else:
            directionY = 0

        actionChain.move_to_element(fromPosition.getOrigin())

        while currentPosition[0] != completeX or currentPosition[1] != completeY:
            actionChain.click_and_hold()
            actionChain.move_by_offset(96 * directionX, 96 * directionY)
            actionChain.release()
            actionChain.move_by_offset(int((96 * directionX) / -1), int((96 * directionY) / -1))

            currentPosition[0] -= directionX
            currentPosition[1] -= directionY

        actionChain.perform()


class MapCell(object):
    NEXT_LEFT = (-1, 0, )
    NEXT_LEFT_TOP = (-1, -1, )
    NEXT_LEFT_BOTTOM = (-1, 1, )

    NEXT_RIGHT = (1, 0, )
    NEXT_RIGHT_TOP = (1, -1, )
    NEXT_RIGHT_BOTTOM = (1, 1, )

    NEXT_TOP = (0, -1, )
    NEXT_BOTTOM = (0, 1, )

    def __init__(self, inst, x, y):
        posX, posY = inst.executeCommand("return require('service/standalone/map').getPosition()")
        x -= posX
        y -= posY

        # if not posX < x < posX + winWidth or not posY < y < posY + winHeight:
        #     raise Exception('Map position %(x)sx%(y)s is invisible for user' % {"x": x, "y": y})

        mapHTMLItem = inst.byCssSelector('#td-%sx%s' % (x, y))

        self.__inst = inst
        self.__item = mapHTMLItem
        self.__x = x
        self.__y = y
        self.__classList = mapHTMLItem.get_attribute('class').split(' ')
        self.__html = mapHTMLItem.get_attribute('innerHTML')
        self.__lxml = None

    def getItem(self):
        return self.__item

    def getPosition(self):
        return (self.__x, self.__y, )

    def getNext(self, nextMap):
        assert type(nextMap) is tuple and len(nextMap) == 2
        x = self.__x + nextMap[0]
        y = self.__y + nextMap[1]

        return MapCell(self.__inst, x, y)

    def getDomain(self):
        return Map_Factory.getDomainById(
            MapCoordinate(x=self.__x, y=self.__y).getPosId()
        )

    def getLand(self):
        for i in self.__classList:
            if i[0:4] == 'land':
                landType, landNumber = i.replace('land-', '').split('-')
                return (landType, landNumber, )

        return (None, None, )

    def isHidden(self):
        return self.__classList[0] == 'shadow'

    def getContainer(self, containerId):
        return self.__item.byCss('div.container[data-id="%s"]' % str(containerId))

    def __loadLXML(self):
        if self.__lxml is None:
            self.__lxml = lxml.html.document_fromstring(self.__html)
