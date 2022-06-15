# -*- coding: utf-8 -*-

name = "vfxDatabaseORM"
version = "1.0.0"
authors = ["Laurette Alexandre"]

requires = ["six", "shotgunPythonApi-3.2", "python-2.7+"]

def commands():
    env.PYTHONPATH.append("{root}")
