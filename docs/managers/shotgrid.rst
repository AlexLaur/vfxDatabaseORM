########
Shotgrid
########

************
Presentation
************

vfxDatabaseORM works pretty fine with Shotgrid. The manager class for Shotgrid can used by importing it.

``from vfxDatabaseORM.adapters.shotgridManager import ShotgridManager``

**Declaration**::

   from vfxDatabaseORM.core import models
   from vfxDatabaseORM.adapters.shotgridManager import ShotgridManager

   class StudioManager(ShotgridManager):
      HOST = "https://my-site.shotgunstudio.com"
      SCRIPT_NAME = "rhendriks"
      SCRIPT_KEY = "c0mPre$Hi0n"
      HTTP_PROXY = ""

   class Project(models.Model):
      manager_class = StudioManager

      name = models.StringField("name")
      users = models.OneToManyField("users", to="User", related_db_name="projects")

   class User(models.Model):
      manager_class = StudioManager

      login = models.StringField("name")
      projects = models.OneToManyField("projects", to="Project", related_db_name="users")

**Example**::

    # Get all projects
    projects = Project.objects.all()

    # Get a project
    project = Project.objects.get(uid=1)

    # Filter projects
    projects = Project.objects.filters(uid__gt=5, name__startswith="Project")

    # Complex filters
    projects = Project.objects.filters(
        uid__gt=5,
        uid__lt=10,
        name__startwith="Project",
        name__contains="Shotgrid",
        users__uid__is=3
    )

    # Update project
    project = Project.objects.get(uid=1)
    project.name = "Foo Project"
    project.save()

    # Other way to update project
    project = Project.objects.get(uid=1)
    project.save(name="Foo Project")

    # Create project
    project = Project(name="Bar Project")
    project.save()  # Store it into the database

    # Create the object in the database in one step
    project = Project.objects.create(name="Bar Project")

    # Delete the project
    project = Project.objects.get(uid=1)
    project.delete()

***********
Limitations
***********

There is an error when we try to retrieve the parent on a OneToManyField.

**Example**::

    project.sequences  # works fine (return all sequences of the project)
    sequence.project  # doesn't work.
