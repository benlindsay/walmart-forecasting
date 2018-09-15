#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# evaluate.py
# 
# Copyright (c) 2018 Ben Lindsay <benjlindsay@gmail.com>

import numpy as np


def wmae(y_pred, y_actual, is_holiday=None, holiday_weight=5):
    """Compute weighted mean average error"""
    if is_holiday is None:
        test_df = load_test_df()
        is_holiday = test_df['IsHoliday']
    n = len(y_pred)
    assert(n == len(y_actual))
    assert(n == len(is_holiday))
    weights = np.ones(n)
    weights[is_holiday] = holiday_weight
    return 1.0 / np.sum(weights) * np.sum(weights * np.abs(y_actual - y_pred))