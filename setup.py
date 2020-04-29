#!/usr/bin/env python3

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

try:
    from sphinx.setup_command import BuildDoc
except ModuleNotFoundError:
    BuildDoc = None


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name="jco2meter",
    description="CO2monitor vfilimonov/co2meter converted to Splunk HEC gizmo",
    author="Paul Miller",
    author_email="paul@jettero.pl",
    url="https://github.com/jettero/co2meter",
    packages=find_packages(),
    cmdclass={"test": PyTest},
    tests_require=["pytest"],
    setup_requires=["setuptools_scm"],
    use_scm_version={
        "write_to": "co2meter/__version__.py",
        # NOTE: use ./setup.py --version to regenerate version.py and print the
        # computed version
    },
    entry_points={"console_scripts": ["jco2meter = jco2meter.cmd:run",],},
)
