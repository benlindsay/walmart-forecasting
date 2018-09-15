#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# models.py
# 
# Copyright (c) 2018 Ben Lindsay <benjlindsay@gmail.com>

import pandas as pd
from datetime import timedelta

from .features import make_id_column
from .transform import get_week_by_dept_df
from .transform import unpivot_week_by_dept_df


class PrevYearBaseline():
    def __init__(self, fillna_method='interpolate'):
        self.fillna_method = fillna_method
    
    def fit(self, X):
        """Given X with columns 'Store', 'Dept', 'Date', and 'Weekly_Sales',
        save data to be accessed by predict
        """
        self.week_by_dept = get_week_by_dept_df(X, fillna_method=self.fillna_method)
    
    def predict(self, X, return_pivoted=False):
        """Given X with columns 'Store', 'Dept', and 'Date', predict 'Weekly_Sales'
        """
        X = make_id_column(X)
        pred_week_by_dept = get_week_by_dept_df(X, fillna_method=None, values=None)
        for c in pred_week_by_dept.columns:
            if c not in self.week_by_dept.columns:
                self.week_by_dept[c] = self.week_by_dept.mean(axis=1)
        
        copy_week_by_dept = self.week_by_dept[pred_week_by_dept.columns.tolist()].copy()
        copy_week_by_dept.index += timedelta(weeks=52)
        pred_week_by_dept = copy_week_by_dept.loc[pred_week_by_dept.index]
        if return_pivoted:
            return pred_week_by_dept
        else:
            unpivoted = unpivot_week_by_dept_df(pred_week_by_dept)
            unpivoted = make_id_column(unpivoted)
            unpivoted = unpivoted.set_index('Id', drop=True)
            unpivoted = unpivoted.reindex(X['Id'])
            return unpivoted['Weekly_Sales']