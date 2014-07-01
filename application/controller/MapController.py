import service.Map


class AbstractMapController:
    def _getAclJsonPackMapService(self):
        return service.Map.Service_Map().decorate('Acl', 'JsonPack')


class MainController(AbstractMapController):
    def load_chunks(self, transfer, data):
        service = self._getAclJsonPackMapService()
        userCollectionChunks = service.getUsersChanks(
            transfer.getUser(),
            data['chunkList']
        )

        transfer.send('/', {
            'done': True,
            'result': {
                'data': userCollectionChunks
            }
        })