class FieldNotFound(Exception):
    pass


class ReadOnlyField(Exception):
    pass


class FieldBadType(Exception):
    pass


class FieldBadValue(Exception):
    pass


class InvalidLookUp(Exception):
    pass


class ModelNotDefined(Exception):
    pass


class ModelNotRegistered(Exception):
    pass


class ManagerNotDefined(Exception):
    pass