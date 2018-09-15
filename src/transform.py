#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# transform.py
# 
# Copyright (c) 2018 Ben Lindsay <benjlindsay@gmail.com>

from .load import load_train_df
from .features import join_columns
import pandas as pd


def get_week_by_dept_df(train_df=None, values='Weekly_Sales',
                        fillna_method='interpolate'):
    if train_df is None:
        train_df = load_train_df()
    if values is None:
        train_df['zeros'] = 0
        fillna_method = None
        values = 'zeros'
    if 'Store_Dept' not in train_df.columns:
        train_df = join_columns(train_df, ['Store', 'Dept'])
    week_by_dept = pd.pivot_table(
        train_df, index='Date', columns='Store_Dept', values=values
    )
    if fillna_method == 'interpolate':
        week_by_dept = week_by_dept.interpolate(limit_direction='both')
    return week_by_dept


def unpivot_week_by_dept_df(week_by_dept, value_name='Weekly_Sales'):
    value_vars = week_by_dept.columns
    week_by_dept = week_by_dept.reset_index().copy()
    unpivoted = pd.melt(week_by_dept, id_vars=['Date'], value_vars=value_vars,
                        value_name=value_name)
    return unpivoted
