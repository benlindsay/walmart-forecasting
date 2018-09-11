#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Ben Lindsay <benjlindsay@gmail.com>

import argparse
import logging
import pandas as pd
from dotenv import find_dotenv
from dotenv import load_dotenv
from os import makedirs
from os.path import dirname
from os.path import exists
from os.path import getmtime
from os.path import isfile
from os.path import join
from urllib.request import urlopen

PROJECT_DIR = dirname(find_dotenv())


def is_current(target, dependencies=[]):
    """Check if target file is current. Returns True if it exists and has
    a modification time after all dependencies.

    Params
    ------
    target : string
        Absolute path of target file
    dependencies : list
        List of absolute paths of files the target depends on

    Returns
    -------
    is_current : boolean
        True if target is current, False if it needs to be updated
    """
    if not isfile(target):
        return False
    if len(dependencies) == 0:
        return True
    for f in dependencies:
        if getmtime(f) > getmtime(target):
            return False
    return True


def download_raw_data(download_url, raw_data_file):
    """Download raw data from URL

    Params
    ------
    download_url : string
        full url of file to download
    raw_data_file : string
        absolute path of file to write to
    """
    raw_data = urlopen(download_url)
    makedirs(dirname(raw_data_file), exist_ok=True)
    with open(raw_data_file, 'w') as output:
        output.write(raw_data.read().decode('utf-8'))


def process_raw_data(raw_data_file, processed_data_file):
    """Process raw data (usually in /data/raw) and write to
    processed_data_file (usually in /data/processed).

    Params
    ------
    raw_data_file : string
        Path to raw data file
    processed_data_file : string
        Path to processed_data_file
    """
    df = pd.read_csv(raw_data_file)
    makedirs(dirname(processed_data_file), exist_ok=True)
    df.to_csv(processed_data_file)


def main(args):
    """ Runs scripts to download raw data into /data/raw then clean and process
    into /data/processed
    """
    logger = logging.getLogger(__name__)

    if is_current(args.raw_data_file):
        logger.info('raw data set already made')
    else:
        logger.info('making raw data set')
        download_raw_data(args.download_url, args.raw_data_file)

    if is_current(args.processed_data_file, [args.raw_data_file]):
        logger.info('final data set already made')
    else:
        logger.info('making final data set from raw data')
        process_raw_data(args.raw_data_file, args.processed_data_file)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    parser = argparse.ArgumentParser(
        description="Process raw data from /data/raw and save in "
                    "/data/processed"
    )
    parser.add_argument('download_url', type=str)
    parser.add_argument('raw_data_file', type=str)
    parser.add_argument('-p', '--processed_data_file', type=str)
    args = parser.parse_args()
    if args.processed_data_file is None:
        args.processed_data_file = args.raw_data_file.replace(
            '/raw/', '/processed/'
        )

    main(args)
