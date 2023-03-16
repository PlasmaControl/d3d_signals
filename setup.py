#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from setuptools import setup

setup(
    name = "d3d_signals",
    version = "0.1.0",
    description = "Mappings from D3D MDS/PTdata signal names to shortcut identifiers",
    url = "https://github.com/PlasmaControl/d3d_signals",
    author = "Ralph Kube",
    author_email = "ralph_kube@gmx.net",
    packages = ["d3d_signals"],
    package_data = {"": ["*.yaml"]},
    install_requires = ["pyyaml"],
    classifiers = [
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        "Programming Language :: Python :: 3.10"
    ],
)


# end of file setup.py