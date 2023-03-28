###########
Serializers
###########

************
Presentation
************

Each models include a serializer.

Two serializers are provided ``JSONSerializer`` and ``PickleSerializer``.

Related fields are not included in the serialized data.

***********
Serializers
***********

.. toctree::
    :maxdepth: 2

    serializers/jsonserializer
    serializers/pickleserializer

*******************************
Override the default serializer
*******************************

By default it is the ``JSONSerializer``.

**Example**::

    from vfxDatabaseORM.core import models
    from vfxDatabaseORM.core.serializers import PickleSerializer

    class Project(models.Model):
        serializer_class = PickleSerializer

        name = models.StringField("name")
        users = models.OneToManyField("users", to="User", related_db_name="projects")

**************************
Create your own serializer
**************************

You can create your own serializer and give it to models.

**Example**::

    from vfxDatabaseORM.core.interfaces import ISerializer

    class MySerializer(ISerializer):

        def serialize(self, model):
            # Serialize the given model instane to data
            return

        def deserialize(self, data):
            # Deserialize the given data to get a model instance
            return
