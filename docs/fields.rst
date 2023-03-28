######
Fields
######

.. _fields:

******
Fields
******

Fields represents a field in a Table. See also :ref:`model`.

You have two types of fields:

- static
- related

*************
Static Fields
*************

.. autoclass:: vfxDatabaseORM.core.models::IntegerField
   :members:
   :special-members: __init__

.. autoclass:: vfxDatabaseORM.core.models::StringField
   :members:
   :special-members: __init__

.. autoclass:: vfxDatabaseORM.core.models::FloatField
   :members:
   :special-members: __init__

.. autoclass:: vfxDatabaseORM.core.models::BooleanField
   :members:
   :special-members: __init__

.. autoclass:: vfxDatabaseORM.core.models::ListField
   :members:
   :special-members: __init__

.. autoclass:: vfxDatabaseORM.core.models::DateTimeField
   :members:
   :special-members: __init__

.. autoclass:: vfxDatabaseORM.core.models::DateField
   :members:
   :special-members: __init__


**************
Related Fields
**************

.. autoclass:: vfxDatabaseORM.core.models::OneToOneField
   :members:
   :inherited-members:
   :special-members: __init__

.. autoclass:: vfxDatabaseORM.core.models::ManyToManyField
   :members:
   :inherited-members:
   :special-members: __init__

.. autoclass:: vfxDatabaseORM.core.models::OneToManyField
   :members:
   :inherited-members:
   :special-members: __init__


*************
Custom Fields
*************

You can create your own fields.

- If you need to create a static field, you should inherit of ``Field``.
- If you need to create a related field, you should inherit of ``RelatedField``.

**Example**::

    from vfxDatabaseORM.core.models.fields import Field, RelatedField

    class MyCustomStaticField(Field):
        pass

    class MyCustomRelatedField(RelatedField):
        pass