[![Python 2.7 3.x](https://img.shields.io/badge/python-2.7%20%7C%203.x-blue.svg)](https://www.python.org/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Coverage](https://img.shields.io/badge/coverage-99%25-green)](#run-coverage-and-tests)
# vfxDatabaseORM

vfxDatabaseORM is a package designed to make some CRUD requests to your Asset Manager.

You can easily integrate another solution like `Ftrack`, `Kitsu` or your own solution by creating the corresponding `Manager`.
It is designed like the powerful Django ORM.

# Advantages
- Easily integration with Asset Managers or Homemade database


The following exemple demonstrates a use case with `Shotgrid`.

```python
from vfxDatabaseORM.core import models
from vfxDatabaseORM.adapters.shotgridManager import ShotgridManager


class MyShotgridManager(ShotgridManager):
    HOST = "https://xxxx.shotgunstudio.com"
    SCRIPT_NAME = "script_name"
    SCRIPT_KEY = "script_key"


class Project(models.Model):
    manager_class = MyShotgridManager  # Manager for SG
    entity_name = "Project"  # Entity name on SG

    uid = models.IntegerField("id", read_only=True, default=-1) # The uid field is "id" on SG
    code = models.StringField("name") # The code field is "name" on SG
    created_at = models.DateTimeField("created_at", read_only=True)

    users = models.OneToManyField("users", to="User", related_db_name="projects")

class User(models.Model):
    manager_class = MyShotgridManager
    entity_name = "HumanUser"

    uid = models.IntegerField("id", read_only=True, default=-1)
    login = models.StringField("login")
    projects = models.OneToManyField("projects", to="Project", related_db_name="users")
```

# Models
Each model representes an entity in the database. When we retrieve an entity, we can access to its attributes.

```python
project = Project.objects.get(uid=2)  # Get the project of id 2
project.uid  # 2
project.code  # foo
project.users  # list of users [<User uid=1>, <User uid=2>]
```

Related attributes are evaluated only when we try to access to them.

```python
# users is a related field linked with the User Model.
# A request to the database is done only when we get the value for this attribute
project.users  # Will produce a request to the database
project.uid  # The value is directly returned
```
# CREATE

Examples of `Create` operations.

```python
new_project = Project.objects.create(code="foo") # Create and store it in the DB
new_project.uid  # The id of the created project in the database.
# or
new_project = Project(code="foo") # Created but not stored in the DB
new_project.uid  # -1 (default value defined in the field)
new_project.save() # Store it in the DB
new_project.uid  # The id of the created project in the database.
```

# READ

Examples of `Read` operations.

```python
# Get all projects
Project.objects.all()

# Get the project where the id to 2
Project.objects.get(uid=2)  # Return an instance of the project
Project.objects.filters(uid=2)  # Return a list of instances
Project.objects.filters(uid__is=2)  # Return a list of instances

# Get all projects where the id is > 500
Project.objects.filters(uid__gt=500)

# Get all projects where the id is > 500 and code ends with "foo"
Project.objects.filters(uid__gt=500, code__endswith="foo")

# Get all projects where the user with id (1) is in the project
Project.objects.filters(users__uid__is=1)

# Get all projects where the user with id (1) is in the project and the code of the project starts with "bar"
Project.objects.filters(users__uid__is=1, code__startswith="bar")

# Get all projects where the user with id (1) in the project, code starts with "baz", code ends with "foo" and id > to 500
Project.objects.filters(users__uid__is=1, code__startswith="baz", code__endswith="foo", uid__gt=500)
```

# UPDATE

Examples of `Update` operations.

```python
project.code = "foo"
project.save() # Update the code in the database
# OR
project.save(code="bar")
```

# DELETE

Examples of `Delete` operations.

```python
project.delete()
```

# TODO
- Add other adapters (Ftrack, Kitsu, DBs)
- Add serializers to serialize a model instance

# Run coverage and tests
Unit tests:
```bash
python -m unittest discover
```

Coverage :
```bash
coverage run -m unittest discover
coverage report -m --skip-covered --skip-empty
```
