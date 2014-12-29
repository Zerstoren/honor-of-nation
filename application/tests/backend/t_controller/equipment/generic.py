from tests.backend.t_controller.generic import Backend_Controller_Generic

from tests.package.db.equipment import Equipment

class Backend_Controller_Equipment_Generic(
    Backend_Controller_Generic,
    Equipment
):
    pass
