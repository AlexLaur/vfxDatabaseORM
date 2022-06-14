# vfxDatabaseORM

vfxDatabaseORM is a package designed to make some CRUD requests to your Asset Manager.

The following exemple demonstrates a use case with `Shotgrid`.

```python
from vfxDatabase.src.domain.models import Model, IntegerField, StringField
from vfxDatabase.src.adapters.shotgunManagerAdapter import ShotgunManagerAdapter


class MyShotgunManager(ShotgunManagerAdapter):
    HOST = "https://xxxx.shotgunstudio.com"
    SCRIPT_NAME = "script_name"
    SCRIPT_KEY = "script_key"


class Project(Model):
    manager_class = MyShotgunManager  # Manager for SG
    entity_name = "Project"  # Entity name on SG

    uid = IntegerField("id", read_only=True, default=-1) # The uid field is "id" on SG
    code = StringField("name") # The code field is "name" on SG
    status = StringField("sg_status_list", default="ip")  # The status field is "sg_status_list" on SG

# CREATE
new_project = Project.create(name="Foo", status="Active") # Create and store it in the DB
# or
new_project = Project(name="Foo", status="Active") # Created but not stored in the DB
new_project.save() # Store it in the DB

# READ
project = Project.objects.get(uid=941)
all_projects = Project.objects.all()
filtered_projects = Project.objects.filters(uid__lt=1000, uid__gt=900, name__startswith="Pipeline")

# UPDATE
project.code = "Hello World"
project.save() # Update the code
# or
project.save(status="fin")

# DELETE
project.delete()
```
