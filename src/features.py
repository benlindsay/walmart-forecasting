#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# features.py
# 
# Copyright (c) 2018 Ben Lindsay <benjlindsay@gmail.com>

def join_columns(df, column_names, delim='_'):
    """Join columns with a delimiter"""
    new_column = delim.join(column_names)
    df = df.copy()
    df[new_column] = df[column_names[0]].map(str)
    for c in column_names[1:]:
        df[new_column] += delim + df[c].map(str)
    return df


def make_id_column(df, store_dept_sep='_'):
    df = df.copy()
    store_dept_col_name = 'Store' + store_dept_sep + 'Dept'
    if store_dept_col_name not in df.columns:
        df = join_columns(df, ['Store', 'Dept'], delim=store_dept_sep)
    df['Id'] = df[store_dept_col_name] + df['Date'].dt.strftime("_%Y-%m-%d")
    return df
