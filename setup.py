#! /usr/bin/env python3

import os, shutil, glob
from setuptools import setup, Command

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""

    CLEAN_FILES = ('./build', './dist', './*.pyc', './*.tgz', './*.egg-info')
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        root = os.path.dirname(__file__)
        for path in self.CLEAN_FILES:
            path = os.path.normpath(os.path.join(root, path))
            for path in glob.glob(path):
                print('removing {}'.format(os.path.relpath(path)))
                shutil.rmtree(path, ignore_errors=True)

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name = 'graph',
    fullname = 'Graph blank for competition tasks',
    version = '0.0.1',
    author = 'Denis Stepnov',
    author_email = 'stepnovdenis@gmail.com',
    url = 'https://github.com/smurphik/graph',
    description = 'Graph blank for competition tasks',
    long_description = read('README.md'),
    long_description_content_type = 'text/markdown',
    license = 'GPLv3',
    keywords = 'graphs',
    py_modules = ['graph'],
    cmdclass = {'clean': CleanCommand},
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)

