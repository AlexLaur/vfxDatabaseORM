class FieldNotFound(Exception):
    pass


class ReadOnlyField(Exception):
    pass


class FieldBadType(Exception):
    pass


class FieldBadValue(Exception):
    pass


class FieldBadAttribute(Exception):
    pass


class InvalidLookUp(Exception):
    pass


class ModelNotDefined(Exception):
    pass


class ModelNotInstantiated(Exception):
    pass


class ModelNotRegistered(Exception):
    pass


class ManagerNotDefined(Exception):
    pass