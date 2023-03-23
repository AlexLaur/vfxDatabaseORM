# -*- coding: utf-8 -*-

name = "vfxDatabaseORM"
version = "1.0.0"
authors = ["Laurette Alexandre"]

requires = [
    "six",
    "networkx",
    "python-2.7+",
    # "~shotgunPythonApi-3.2",  # Replace by your REZ package name for SG API
    # "~ftrackPythonApi-2.4",  # Replace by your REZ package name for FTrack API
]


def commands():
    env.PYTHONPATH.append("{root}")
