import abc

ABC = abc.ABCMeta("ABC", (object,), {})


class IManager(ABC):
    def __init__(self, model_class):
        self.model_class = model_class

    @abc.abstractmethod
    def get(self, uid):
        pass

    @abc.abstractmethod
    def all(self):
        pass

    @abc.abstractmethod
    def filters(self, **kwargs):
        pass

    @abc.abstractmethod
    def create(self, **kwargs):
        pass

    @abc.abstractmethod
    def insert(self, instance):
        pass

    @abc.abstractmethod
    def update(self, instance):
        pass

    @abc.abstractmethod
    def delete(self):
        pass
