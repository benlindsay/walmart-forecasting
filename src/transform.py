#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# transform.py
# 
# Copyright (c) 2018 Ben Lindsay <benjlindsay@gmail.com>

import numpy as np
import pandas as pd

from .load import load_train_df
from .features import join_columns


def get_week_by_dept_df(train_df=None, values='Weekly_Sales',
                        fillna_method='interpolate', store_dept_sep='_'):
    if train_df is None:
        train_df = load_train_df(store_dept_sep=store_dept_sep)
    if values is None:
        train_df['zeros'] = 0
        fillna_method = None
        values = 'zeros'
    store_dept_col_name = 'Store' + store_dept_sep + 'Dept'
    if store_dept_col_name not in train_df.columns:
        train_df = join_columns(train_df, ['Store', 'Dept'],
                                delim=store_dept_sep)
    week_by_dept = pd.pivot_table(
        train_df, index='Date', columns=store_dept_col_name, values=values
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


def svd_reconstruct(df, n_comp=10):
    df = df.copy()
    u, s, vh = np.linalg.svd(df)
    df.iloc[:, :] = (u[:, :n_comp] * s[:n_comp]) @ vh[:n_comp, :]
    return df
