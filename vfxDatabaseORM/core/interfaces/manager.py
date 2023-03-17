class IManager(object):
    def __init__(self, model_class):
        self.model_class = model_class

    def get(self, uid):
        pass

    def all(self):
        pass

    def filters(self, **kwargs):
        pass

    def create(self, data):
        pass

    def update(self, uid, new_data):
        pass

    def delete(self):
        pass
