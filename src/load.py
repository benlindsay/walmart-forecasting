#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# load.py
# 
# Copyright (c) 2018 Ben Lindsay <benjlindsay@gmail.com>

from dotenv import find_dotenv
from os.path import dirname
from os.path import join
import pandas as pd

from .features import join_columns

# Root directory of repo
project_dir = dirname(find_dotenv())

def load_train_df(store_dept_sep='_'):
    train_csv = join(project_dir, 'data/raw/train.csv')
    train_df = pd.read_csv(train_csv, parse_dates=[2])
    train_df = join_columns(train_df, ['Store', 'Dept'],
                            delim=store_dept_sep)
    return train_df

def load_test_df():
    test_csv = join(project_dir, 'data/raw/test.csv')
    test_df = pd.read_csv(test_csv, parse_dates=[2])
    test_df = join_columns(test_df, ['Store', 'Dept'])
    return test_df
