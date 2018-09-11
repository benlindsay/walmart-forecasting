#!/bin/bash
#
# startup.sh
#
# Copyright (c) 2018 Ben Lindsay <benjlindsay@gmail.com>

touch .env
make data
gunicorn dash-app:server --log-file -
