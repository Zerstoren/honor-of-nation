import service.Map
import service.MapUserVisible

class AbstractMapController:
    def _getAclJsonPackMapService(self):
        return service.Map.Service_Map().decorate('JsonPack')

    def _getMapUserVisibleService(self):
        return service.MapUserVisible.Service_MapUserVisible()


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