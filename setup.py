
# ==================================================================================
# MIT License

# Copyright (c) 2022 Emmadi Sumith Kumar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#====================================================================================

from codecs import open
from os.path import abspath, dirname, join , expanduser

from setuptools import Command, find_packages, setup

this_dir = abspath(dirname(__file__))

with open(join(this_dir, "truecallerpy","version.txt"), encoding='utf-8') as versionFile:
    version = versionFile.read()

with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name = 'truecallerpy',
    version = version,
    description = "A package to find phone number details",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/sumithemmadi/truecallerpy',
    author = 'Sumith Emmadi',
    author_email = 'sumithemmadi244@gmail.com',
    maintainer = "Sumith Emmadi",
    maintainer_email = "sumithemmadi244@gmail.com",
    license = 'MIT',
    license_file = "LICENSE",
    platforms = "any",

    classifiers = [
        'Topic :: Utilities',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6'
    ],
    keywords = ['truecaller' , 'search' , 'number' , 'phone' , 'find' , 'email' , 'truecallerpy' , 'brute' , 'address' , 'force' , 'attack' , 'spy'],
    packages = find_packages(exclude=[ 'tests*']),
    include_package_data=True,
    install_requires = ['requests',"phonenumbers"],
    entry_points = {
        'console_scripts': [
            'truecallerpy=truecallerpy:ExecuteTrurcallerPy',
        ],
    },

)
