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
> Note: Field `id` is implicit (used in major databases system).
> You can get it with: `instance.uid`

> If you need to redefine it, you can by adding : `uid = models.IntegerField("id", default=0)` into yours models.

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

    code = models.StringField("name") # The code field is "name" on SG
    created_at = models.DateTimeField("created_at", read_only=True)

    users = models.OneToManyField("users", to="User", related_db_name="projects")

class User(models.Model):
    manager_class = MyShotgridManager
    entity_name = "HumanUser"

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
project.users  # Will send a request to the database
project.uid  # The value is directly returned
```
# CREATE

Examples of `Create` operations.

```python
new_project = Project.objects.create(code="foo") # Create and store it in the DB
new_project.uid  # The id of the created project in the database.
# or
new_project = Project(code="foo") # Created but not stored in the DB
new_project.uid  # 0 (default value defined in the field)
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
project.code = "foo" # Update the code only in the instance
project.save() # Update the code in the database
# OR
project.save(code="bar") # Update the code in the database
```

# DELETE

Examples of `Delete` operations.

```python
project.delete()  # Delete the project in the database
```

# Serializers

By default, each `Model` has a JSON serializer.
Some serializers are defined in `vfxDatabaseORM.core.serializers`.

- JSONSerializer
- PickleSerializer

```python
class Project(models.Model):
    manager_class = MyCustomManager

    uid = models.IntegerField("id", read_only=True)
    code = models.StringField("code")


project = Project(uid=50, code="foo")

# Serialize
data = Project.serializer.serialize(project)  # {"uid": 50, "code": "foo"}

# De-Serialize
new_instance = Project.serializer.deserialize(data)

assert project == new_instance
```

You can override the serializer with the attribute `serializer_class`.
```python
class Project(models.Model):
    manager_class = MyCustomManager
    serializer_class = MyCustomSerializer

    uid = models.IntegerField("id", read_only=True)
    code = models.StringField("code")
```

# TODO
- Add other adapters (Ftrack, Kitsu, DBs)
- Add the update for related fields
- Serialize in depth ?


# Build the doc
```bash
cd docs/
./make.bat html  # On Windows
make html  # On UNIX
```

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
