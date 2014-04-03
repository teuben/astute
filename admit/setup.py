#

import os


## two ways to do it ?
from setuptools import setup
# from distutils.core import setup



# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# the required stuff (the version= also should be in the Makefile, for proper labeling)
setup(
    name = "admit",
    version = "0.0.2",
    author = "Peter Teuben",
    author_email = "teuben@gmail.com",
    description = ("A test precursor for ADMIT."),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://carma.astro.umd.edu/wiki/index.php/ADMIT",
    packages=['admit', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
