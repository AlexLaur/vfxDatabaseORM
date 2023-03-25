#####
Model
#####

.. _model:

*****
Model
*****

Model represents a Table in the database.

A Table contains :ref:`fields`.

.. note:: Model implements the ``uid`` field. But you can redefine it if needed.

*************
Documentation
*************

.. autoclass:: vfxDatabaseORM.core.models::Model
   :members:


****
Demo
****

**Example**::

    from vfxDatabaseORM.core.models import Model
    from vfxDatabaseORM.core.interfaces import IManager

    class StudioManager(IManager):
        # Manager only for the example
        pass

    class Project(models.Model):
        manager_class = StudioManager

        name = models.StringField("name")
        users = models.OneToManyField("users", to="User", related_db_name="projects")

   class User(models.Model):
        manager_class = StudioManager

        login = models.StringField("name")
        projects = models.OneToManyField("projects", to="Project", related_db_name="users")