from tests.backend.t_models.generic import Backend_Models_Generic

from tests.data.Map import Kit


class Backend_Models_Map_Generic(Backend_Models_Generic):
    def _createMapCell(self, x=40, y=40, land=None):
        kit = Kit.Create()
        mapDomain = kit.getDomain()

        setters = kit.getSetters()
        decorator = kit.wrap(kit.getDefaultDecorator(), [
            setters.Position(x, y),
            setters.Land(land if land else mapDomain.LAND_VALLEY),
            setters.Add()
        ])

        decorator(mapDomain.edit())

        return mapDomain
