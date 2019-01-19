#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Jon Zhang 
@contact: zj.fly100@gmail.com
@site: 

@version: 1.0
@license: 
@file: matchfile.py
@time: 2019-1-19 21:39

the line began to write the explanation and demonstration of this document
"""

# coding:gbk
import logging
import logging.config
import os
import json
from filecmp import dircmp

def SetupLogging(default_path='logging.json', default_level=logging.debug,env_key='LOG_CFG'):
    """Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def show_diff_files(dcmp):
    for name in dcmp.diff_files:
        logger.info("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        show_diff_files(sub_dcmp)


def show_only(dcmp):
    if dcmp.left_only:
        ave_rst = 1
        for i in dcmp.left_only:
            logger.info("%s只存在于%s中" % (i, dcmp.left))

    if dcmp.right_only:
        for i in dcmp.right_only:
            logger.info("%s只存在于%s中" % (i, dcmp.right))

    for sub_dcmp in dcmp.subdirs.values():
        show_only(sub_dcmp)


def compare(dir1, dir2):
    dcmp = dircmp(dir1, dir2)
    show_diff_files(dcmp)
    show_only(dcmp)


if __name__ == "__main__":
    SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
    logger = logging.getLogger(__name__)
    dir1 = input("Please input the f1 name:")
    dir2 = input("Please input the f2 name:")
    compare(dir1, dir2)
