"""Setup for IIIF Presentation API implementation."""
from setuptools import setup, Command
import os
import sys
# setuptools used instead of distutils.core so that 
# dependencies can be handled automatically

# Extract version number from iiif_prezi/_version.py. Here we are very strict
# about the format of the version string as an extra sanity check.
# (thanks for comments in 
# http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package )
import re
VERSIONFILE="iiif_prezi/_version.py"
verfilestr = open(VERSIONFILE, "rt").read()
match = re.search(r"^__version__ = '(\d\.\d.\d+(\.\d+)?)'", verfilestr, re.MULTILINE)
if match:
    version = match.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE))

class Coverage(Command):
    """Class to allow coverage run from setup."""

    description = "run coverage"
    user_options = []

    def initialize_options(self):
        """Empty initialize_options."""
        pass

    def finalize_options(self):
        """Empty finalize_options."""
        pass

    def run(self):
        """Run coverage program."""
        os.system("coverage run --source=iiif_prezi setup.py test")
        os.system("coverage report")
        os.system("coverage html")
        print("See htmlcov/index.html for details.")

install_requires=[
    "lxml",
    "Pillow>=3.2.0,<4.0.0",  # Pillow 4.0.0 drops python 2.6 support
    "pyld",
]
if (sys.version_info[0:2] < (2,7)):
    install_requires.append('ordereddict')
    install_requires.append('future')

setup(
    name='iiif-prezi',
    version=version,
    author='Rob Sanderson, Simeon Warner',
    packages=['iiif_prezi'],
    package_data={
      'iiif_prezi': ['contexts/*.json'],
    },
    classifiers=["Development Status :: 4 - Beta",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: Apache Software License",
                 "Operating System :: OS Independent", #is this true? know Linux & OS X ok
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2.6",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3.3",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5",
                 "Topic :: Internet :: WWW/HTTP",
                 "Topic :: Multimedia :: Graphics :: Graphics Conversion",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 "Environment :: Web Environment"],
    url='https://github.com/IIIF/iiif-prezi',
    license='LICENSE.md',
    description='IIIF Presentation API implementation',
    long_description=open('README').read(),
    install_requires=install_requires,
    test_suite="tests",
    tests_require=[
        "testfixtures"
    ],
    cmdclass={
        'coverage': Coverage,
    },
)
