###############
JSON Serializer
###############

This is the default serializer for ``Models``.

**Case**::

    from vfxDatabaseORM.core import models

    class Project(models.Model):

        name = models.StringField("name")
        users = models.OneToManyField("users", to="User", related_db_name="projects")


**Example**::

    project = Project(uid=50, name="foo")

    data = Project.serializer.serialize(project)
    print(data)  # {"uid": 50, "name": "foo"}

    new_instance = Project.serilizer.deserialize(data)
    print(new_instance)  # <Project uid=50>

    assert project == new_instance