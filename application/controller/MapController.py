from service.Map import Service_Map
from service.MapUserVisible import Service_MapUserVisible

class AbstractMapController:
    def _getAclJsonPackMapService(self):
        return Service_Map().decorate(Service_Map.JSONPACK)

    def _getMapUserVisibleService(self):
        return Service_MapUserVisible()


class MainController(AbstractMapController):
    def load_chunks(self, transfer, data):
        userCollectionChunks = self._getAclJsonPackMapService().getByVisibleCollection(
            self._getMapUserVisibleService().getByChunks(
                transfer.getUser(),
                data['chunkList']
            )
        )

        transfer.send('/map/load_chunks', {
            'done': True,
            'result': {
                'data': userCollectionChunks
            }
        })