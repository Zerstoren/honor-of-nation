from . import Abstract
from models.User.Domain import User_Domain

class User_Collection(Abstract.AbstractCollection):
    domain = User_Domain
