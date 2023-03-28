#################
Pickle Serializer
#################


**Case**::

    from vfxDatabaseORM.core import models
    from vfxDatabaseORM.core.serialiers import PickleSerializer

    class Project(models.Model):

        serializer_class = PickleSerializer

        name = models.StringField("name")
        users = models.OneToManyField("users", to="User", related_db_name="projects")


**Example**::

    project = Project(uid=50, name="foo")

    data = Project.serializer.serialize(project)
    print(data)  # pickled data

    new_instance = Project.serilizer.deserialize(data)
    print(new_instance)  # <Project uid=50>

    assert project == new_instance