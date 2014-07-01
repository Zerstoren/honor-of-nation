
class Arguments(Exception):
    pass


class WrongCleanType(TypeError):
    pass


class NotEnoughArguments(Arguments):
    pass


class WrongArgumentType(Arguments):
    pass


class DeepArgumentsError(Arguments):
    pass


class ArgumentIsRequired(Arguments):
    pass


class EnumError(Arguments):
    pass
