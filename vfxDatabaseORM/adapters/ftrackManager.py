import ftrack_api

from vfxDatabaseORM.core.interfaces import IManager
from vfxDatabaseORM.core.factories import ModelFactory


class FTrackManager(IManager):
    HOST = ""
    API_NAME = ""
    API_KEY = ""

    _SESSION = None

    def __init__(self, model_class):
        super(FTrackManager, self).__init__(model_class)

        if not self._SESSION:
            self._SESSION = ftrack_api.Session(
                server_url=self.HOST,
                api_key=self.API_KEY,
                api_user=self.API_NAME,
            )

    def get(self, uid):
        raise NotImplementedError()

    def all(self):
        raise NotImplementedError()

    def filters(self, **kwargs):
        raise NotImplementedError()

    def create(self, instance):
        raise NotImplementedError()

    def update(self, instance):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()
