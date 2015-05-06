from . import abstract

from models.Map.Factory import Map_Factory
from helpers.MapCoordinate import MapCoordinate

from models.Map import Common as MapCommon


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

        body = self.byCssSelector('body')
        offset = self.getMousePosition(fromPosition)
        # actionChain.move_to_element_with_offset(body, offset.x, offset.y)
        self._moveMouseToPosition(actionChain, fromPosition)

        while currentPosition[0] != completeX or currentPosition[1] != completeY:
            actionChain.click_and_hold()
            actionChain.move_by_offset(128 * directionX, 64 * directionY)
            actionChain.release()
            actionChain.moby_offset(int((128 * directionX) / -1), int((64 * directionY) / -1))

            currentPosition[0] -= directionX
            currentPosition[1] -= directionY

        actionChain.perform()

    def getMousePosition(self, mapCell):
        x, y = mapCell.getPosition()
        cameraPos = self.executeCommand("""
        var t = require('service/standalone/map').controller.currentCameraLocation;
        return [t.x, t.y];
        """)

        mapItemPos = {
            "x": x - cameraPos[0],
            "y": y - cameraPos[1]
        }

        pointPosition = self.executeCommand("""
        var point = require('service/standalone/map').controller.projection.toIsometric([%i, %i]);
        return [point.x, point.y];
        """ % (mapItemPos['x'], mapItemPos['y']))

        mapShift = self.executeCommand("""
        var shift = require('service/standalone/map').controller.shift.getShift();
        return [shift.x, shift.y];
        """)

        return {
            'x': pointPosition[0] + mapShift[0] + 64,
            'y': pointPosition[1] + mapShift[1]
        }

    def mapDragNDrop(self, fromMapCell, toMapCell):
        chain = self.getChainAction()
        self._moveMouseToPosition(chain, fromMapCell)
        chain.click_and_hold()
        self._moveMouseToPosition(chain, toMapCell)
        chain.release()
        chain.perform()

    def waitForMapItemLoad(self, x, y):
        i = 0

        while True:
            try:
                result = self.executeCommand("""
                try {
                    return require('service/standalone/map/draw').map[%i][%i];
                } catch(e) {
                    return null;
                }
                """ % (y, x))
                assert result != None
                break
            except (self.WebDriverException, AssertionError):
                i += 1
                if i == 20:
                    raise self.WebDriverException("Can`t load map")

                self.sleep(0.2)

    def mapCenterCamera(self, x, y):
        self.executeCommand("""
        return require('service/standalone/map').setCenterCameraPosition(%i, %i);
        """ % (x, y, ))
        self.waitForMapItemLoad(x, y)

    def _moveMouseToPosition(self, chain, mapCell):
        body = self.byCssSelector('body')
        offset = self.getMousePosition(mapCell)
        chain.move_to_element_with_offset(body, offset['x'], offset['y'])

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
        # posX, posY = inst.executeCommand("""
        #     var cameraPos = require('service/standalone/map').getCameraPosition();
        #     return [cameraPos.x, cameraPos.y];
        # """)

        # if not posX < x < posX + winWidth or not posY < y < posY + winHeight:
        #     raise Exception('Map position %(x)sx%(y)s is invisible for user' % {"x": x, "y": y})

        self.__inst = inst

        self.__item = inst.executeCommand("""
        return require('service/standalone/map/draw').map[%i][%i];
        """ % (y, x))


        self.__x = x
        self.__y = y

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
        return (self.__item[MapCommon.TRANSFER_ALIAS_LAND], self.__item[MapCommon.TRANSFER_ALIAS_LAND_TYPE], )

    def isHidden(self):
        return False

    def click(self):
        chain = self.getMap().getChainAction()
        self.getMap()._moveMouseToPosition(chain, self)
        chain.click()
        chain.perform()

    def getMap(self):
        """
        :rtype: Map
        """
        return self.__inst

    # def getContainer(self, containerId):
    #     return self.__item.byCss('div.container[data-id="%s"]' % str(containerId))
    #
    # def __loadLXML(self):
    #     if self.__lxml is None:
    #         self.__lxml = lxml.html.document_fromstring(self.__html)
