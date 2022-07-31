#!/usr/bin/python
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
from os.path import abspath, dirname, join

def truecallerpy_info():
    this_dir = abspath(dirname(__file__))
    
    with open(join(this_dir,"version.txt"), encoding='utf-8') as versionFile:
        version = versionFile.read()
    data = '''
    truecallerpy
    Version     : {}
    Summary     : A package to find phone number details
    Home-page   : https://github.com/sumithemmadi/truecallerpy
    Author      : Sumith Emmadi
    Author-email: sumithemmadi244@gmail.com
    License     : MIT
    '''.format(version)
    return data

# print(truecallerpy_info())