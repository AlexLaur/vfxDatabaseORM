# -*- coding: utf-8 -*-

name = "vfxDatabaseORM"
version = "1.0.0"
authors = ["Laurette Alexandre"]

requires = [
    "six",
    "networkx",
    "python-2.7+",
    "~shotgunPythonApi-3.2",
]


def commands():
    env.PYTHONPATH.append("{root}")
