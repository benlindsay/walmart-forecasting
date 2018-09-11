#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Ben Lindsay <benjlindsay@gmail.com>

from dotenv import find_dotenv
from os import walk
from os.path import dirname
from os.path import join
import subprocess
import tempfile

PROJECT_DIR = dirname(find_dotenv())


def _exec_notebook(path):
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=1000",
                "--output", fout.name, path]
        subprocess.check_call(args)


def test_nb():
    for root, d_names, f_names in walk(join(PROJECT_DIR, 'notebooks')):
        for f in f_names:
            if f.endswith('.ipynb'):
                _exec_notebook(join(root, f))
