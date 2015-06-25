from . import Abstract
from models.UserState.Domain import UserState_Domain

class UserState_Collection(Abstract.AbstractCollection):
    domain = UserState_Domain
