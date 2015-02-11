from service.Map import Service_Map
from service.MapUserVisible import Service_MapUserVisible
from service.Army import Service_Army

import controller.ArmyController

class AbstractMapController:
    def _getAclMapService(self):
        return Service_Map().decorate(Service_Map.ACL)

    def _getMapUserVisibleService(self):
        return Service_MapUserVisible()


class MainController(AbstractMapController):
    def load_chunks(self, transfer, data):
        userCollectionChunks = self._getAclMapService().getByVisibleCollection(
            self._getMapUserVisibleService().getByChunks(
                transfer.getUser(),
                data['chunkList']
            )
        )

        userChunksList = Service_Map().getDecorateClass(Service_Map.JSONPACK).fromCollectionToList(userCollectionChunks)
        units = Service_Army().decorate(Service_Army.JSONPACK).loadByMapCollection(userCollectionChunks)

        transfer.send('/map/load_chunks', {
            'done': True,
            'result': {
                'data': userChunksList
            }
        })

        controller.ArmyController.DeliveryController().updateUnitsOnMap(transfer.getUser(), units)
