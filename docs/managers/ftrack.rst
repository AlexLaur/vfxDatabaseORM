######
FTrack
######

vfxDatabaseORM has not been tested with FTrack.
The manager class for Ftrack can used by importing it.

``from vfxDatabaseORM.adapters.ftrackManager import FTrackManager``

.. note:: No implementation has been made.

**Declaration**::

    from vfxDatabaseORM.core import models
    from vfxDatabaseORM.adapters.ftrackManager import FTrackManager

    class StudioManager(FTrackManager):
        HOST = "https://mycompany.ftrackapp.com"
        API_NAME = "7545384e-a653-11e1-a82c-f22c11dd25eq"
        API_KEY = "martin"

    class Project(models.Model):
        manager_class = StudioManager

        name = models.StringField("name")
        status = models.StringField("status")

**Example**::
    pass