from . import abstractGeneric

import lxml.html
import json

class Selenium_Generic(abstractGeneric.Selenium_Abstract_Generic):
    def login(self, userDomain=None):
        if userDomain:
            user = userDomain
        else:
            user = self.fixture.getUser(0)

        self.executeCommand("window.localStorage.login = '%s'" % user.getLogin())
        self.executeCommand("window.localStorage.password = '%s'" % user._reservedPasswordForTest)

        self.go('/')
        self.waitForSocket()

    # def moveToPath(self, module, data):
    #     self.serviceAction('$nav', "service.locate('%s', %s);" % (module, json.dumps(data)))
    #
    # def serviceAction(self, serviceName, serviceAction):
    #     return self.executeCommand("""
    #         var service = angular.element('[ng-view]').injector().get('%(serviceName)s');
    #         %(serviceAction)s
    #         """ % {
    #             "serviceName": serviceName,
    #             "serviceAction": serviceAction
    #         })
    #
    # def getPopup(self):
    #     return self.byXPath('//div[@class=\'popup\' and contains(@style, \'block\')]')
    #
    # def _getResources(self):
    #     resourceBlock = self.byCssSelector('.resources')
    #     return {
    #         "rubins": int(resourceBlock.byCss('.rubins').get_attribute('ng-hint').replace(' ', '')),
    #         "steel": int(resourceBlock.byCss('.steel').get_attribute('ng-hint').replace(' ', '')),
    #         "eat": int(resourceBlock.byCss('.eat').get_attribute('ng-hint').replace(' ', '')),
    #         "stone": int(resourceBlock.byCss('.stone').get_attribute('ng-hint').replace(' ', '')),
    #         "wood": int(resourceBlock.byCss('.wood').get_attribute('ng-hint').replace(' ', '')),
    #         "gold": int(resourceBlock.byCss('.gold').get_attribute('ng-hint').replace(' ', '')),
    #     }
    #
    # def _setCameraMapPosition(self, x, y):
    #     self.serviceAction('$map', 'service.setCameraPosition(%d, %d)' % (x, y))
    #
    # def _getMap(self, x, y):
    #     return MapCell(self, x, y)
    #
    # def _doubleClick(self, webElement):
    #     actionChain = self.getChainAction()
    #     actionChain.double_click(webElement)
    #     actionChain.perform()
    #
    # def _contextClick(self, webElement):
    #     actionChain = self.getChainAction()
    #     actionChain.context_click(webElement)
    #     actionChain.perform()
    #
    # def _moveCursor(self, toPosition):
    #     assert isinstance(toPosition, MapCell)
    #
    #     actionChain = self.getChainAction()
    #     actionChain.move_to_element(toPosition.getItem())
    #     actionChain.perform()
    #
    # def _moveCamera(self, fromPosition, toPosition):
    #     assert isinstance(fromPosition, MapCell)
    #     assert isinstance(toPosition, MapCell) or type(toPosition) is tuple
    #
    #     actionChain = self.getChainAction()
    #     startX, startY = fromPosition.getPosition()
    #     completeX, completeY = toPosition if type(toPosition) is tuple else toPosition.getPosition()
    #
    #     currentPosition = [startX, startY, ]
    #
    #     if completeX - startX > 0:
    #         directionX = -1
    #     elif completeX - startX < 0:
    #         directionX = 1
    #     else:
    #         directionX = 0
    #
    #     if completeY - startY > 0:
    #         directionY = -1
    #     elif completeY - startY < 0:
    #         directionY = 1
    #     else:
    #         directionY = 0
    #
    #     actionChain.move_to_element(fromPosition.getOrigin())
    #
    #     while currentPosition[0] != completeX or currentPosition[1] != completeY:
    #         actionChain.click_and_hold()
    #         actionChain.move_by_offset(96 * directionX, 96 * directionY)
    #         actionChain.release()
    #         actionChain.move_by_offset(int((96 * directionX) / -1), int((96 * directionY) / -1))
    #
    #         currentPosition[0] -= directionX
    #         currentPosition[1] -= directionY
    #
    #     actionChain.perform()


# class MapCell(object):
#     NEXT_LEFT = (-1, 0, )
#     NEXT_LEFT_TOP = (-1, -1, )
#     NEXT_LEFT_BOTTOM = (-1, 1, )
#
#     NEXT_RIGHT = (1, 0, )
#     NEXT_RIGHT_TOP = (1, -1, )
#     NEXT_RIGHT_BOTTOM = (1, 1, )
#
#     NEXT_TOP = (0, -1, )
#     NEXT_BOTTOM = (0, 1, )
#
#     def __init__(self, inst, x, y):
#         posX, posY = inst.serviceAction('$map', 'return service.getPosition()')
#         winWidth, winHeight = inst.serviceAction('$map', 'return [service.getMapWidth(), service.getMapHeight()]')
#
#         if not posX < x < posX + winWidth or not posY < y < posY + winHeight:
#             raise Exception('Map position %(x)sx%(y)s is invisible for user' % {"x": x, "y": y})
#
#         mapHTMLItem = inst.byXPath(
#             '//td[@data-position="%(x)dx%(y)d"]' % {
#                 "x": x - posX,
#                 "y": y - posY
#             }
#         )
#
#         self.__inst = inst
#         self.__item = mapHTMLItem
#         self.__x = x
#         self.__y = y
#         self.__classList = mapHTMLItem.get_attribute('class').split(' ')
#         self.__html = mapHTMLItem.get_attribute('innerHTML')
#         self.__lxml = None
#
#     def getItem(self):
#         return self.__item
#
#     def getPosition(self):
#         return (self.__x, self.__y, )
#
#     def getNext(self, nextMap):
#         assert type(nextMap) is tuple and len(nextMap) == 2
#         x = self.__x + nextMap[0]
#         y = self.__y + nextMap[1]
#
#         return MapCell(self.__inst, x, y)
#
#     def getDomain(self):
#         return models.Map.Factory.factory.getByPosition(self.__x, self.__y)
#
#     def getLand(self):
#         for i in self.__classList:
#             if i[0:4] == 'land':
#                 landType, landNumber = i.replace('land-', '').split('-')
#                 return (landType, landNumber, )
#
#         return (None, None, )
#
#     def isHidden(self):
#         return self.__classList[0] == 'shadow'
#
#     def getOrigin(self):
#         return self.__item
#
#     def getContainer(self, containerId):
#         return self.__item.byCss('#container_' + str(containerId))
#
#     def __loadLXML(self):
#         if self.__lxml is None:
#             self.__lxml = lxml.html.document_fromstring(self.__html)
