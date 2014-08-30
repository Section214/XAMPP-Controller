#!/usr/bin/env python

from distutils.core import setup

setup(
    name = "XAMPP Controller",
    version = "1.0",
    description = "A simple XAMPP indicator applet",
    author = "Daniel J Griffiths",
    author_email = "dgriffiths@section214.com",
    url = "http://section214.com",
    license = "GPL",
    package_dir = {"xampp-controller" : "src/xampp-controller"},
    packages = ["xampp-controller"],
    package_data = {"xampp-controller" : [""]},
    data_files = [
        ("share/applications/xampp-controller", [
            "xampp-controller.py",
            "xampp-controller.svg",
            "about-icon.png"
        ]),
        ("bin", ["xampp-controller"]),
    ],
    scripts = ["xampp-controller"],
    long_description = """XAMPP Controller provides a simple indicator
    applet for quick access to XAMPP commands and your websites""",
)
