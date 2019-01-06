#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Jon Zhang 
@contact: zj.fly100@gmail.com
@site: 

@version: 1.0
@license: 
@file: BigDataSwitch.py
@time: 2018-12-22 21:42

the line began to write the explanation and demonstration of this document
"""
import os
import sys
import datetime
import logging
import json
import logging.config
import xml.etree.ElementTree as ET
################################
import pymssql
import cx_Oracle
import MySQLdb


def setup_logging(default_path='logging.json', default_level=logging.debug,env_key='LOG_CFG'):
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


class XmlParse(object):
    def __init__(self, file_path):
        self.tree = None
        self.root = None
        self.xml_file_path = file_path

    def ReadXml(self):
        setup_logging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
        logger = logging.getLogger(__name__)
        try:
            # print("xmlfile:", self.xml_file_path)
            self.tree = ET.parse(self.xml_file_path)
            self.root = self.tree.getroot()
        except Exception as e:
            print("parse xml faild!")
            sys.exit()
        else:
            pass
            logger.debug("parse xml success!")
        finally:
            return self.tree

    def WriteXml(self):
        pass


def connDb(databasetype, ipAdress, userName, userPwd, dbName, listenPort=None):
    if databasetype == 'S':
        conn = pymssql.connect(ipAdress, userName, userPwd, dbName)
        return conn
    elif databasetype == 'O':
        dsn = cx_Oracle.makedsn(ipAdress, listenPort, dbName)
        conn = cx_Oracle.connect(userName, userPwd, dsn)
        return conn
    elif databasetype == 'M':
        conn = MySQLdb.connect(ipAdress, userName, userPwd, dbName, charset='utf8')
        return conn


def selectDB(db, sql, values):
    cursor = db.cursor()
    cursor.execute(sql)
    for result in cursor:
        if values in str(result):
            cursor.close()
            db.close()
            yield True, result
        else:
            cursor.close()
            db.close()
            yield False


def selectDB11(db, sql, values):
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    db.close()
    for result in results:
        if values in str(result):
            yield True, result
        else:
            yield False


def timeer(func):
    def wrapper():
        setup_logging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
        a = datetime.datetime.now()
        func()
        b = datetime.datetime.now()
        logger = logging.getLogger(__name__)
        logger.info("使用时间：%s" % (b - a))
    return wrapper


def ReadMain(XML_NAME):
    setup_logging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
    logger = logging.getLogger(__name__)
    xml_file = os.path.abspath(XML_NAME)
    parse = XmlParse(xml_file)
    tree = parse.ReadXml()
    root = tree.getroot()
    logger.debug(root)
    dict_all_list = {}
    captionList = root.findall("Head")  # 在当前指定目录下遍历
    for caption in captionList:
        logger.debug('caption=====>%s' % caption)
        logger.debug(caption.attrib)
        dict_db_list = caption.attrib
        child_list = caption.findall("Body")
        list_dict_str = []
        logger.debug(child_list)
        for i in range(len(child_list)):
            dict_str = {}
            dict_str[child_list[i].attrib['match_str']] = child_list[i].text
            list_dict_str.append(dict_str)
        logger.debug('list_dict_str--->%s' % list_dict_str)
        dict_all_list[dict_db_list['type']] = [dict_db_list, list_dict_str]
    return dict_all_list


@timeer
def theMain():
    setup_logging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
    logger = logging.getLogger(__name__)
    dict_all_list = ReadMain('EXP_DATA_CONF.xml')
    for i in range(len(dict_all_list.keys())):
        dict_db_list, list_dict_str = dict_all_list[list(dict_all_list.keys())[i]]
        for i in list_dict_str:
            logger.debug(i)
            values = list(i.keys())[0]
            sql = i[values]
            database_type = dict_db_list['database_type']
            ip_adress = dict_db_list['ip_adress']
            user_name = dict_db_list['user_name']
            user_pwd = dict_db_list['user_pwd']
            db_name = dict_db_list['db_name']
            listen_port = dict_db_list['listen_port']
            db = connDb(database_type, ip_adress, user_name, user_pwd, db_name, listen_port)
            res = selectDB(db, sql, values)
            logger = logging.getLogger(__name__)
            logger.info(res.__next__())


# @timeer
# def theMain11():
#     setup_logging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
#     logger = logging.getLogger(__name__)
#     dict_all_list = ReadMain('EXP_DATA_CONF.xml')
#     for i in range(len(dict_all_list.keys())):
#         dict_db_list, list_dict_str = dict_all_list[list(dict_all_list.keys())[i]]
#         for i in list_dict_str:
#             logger.debug(i)
#             values = list(i.keys())[0]
#             sql = i[values]
#             database_type = dict_db_list['database_type']
#             ip_adress = dict_db_list['ip_adress']
#             user_name = dict_db_list['user_name']
#             user_pwd = dict_db_list['user_pwd']
#             db_name = dict_db_list['db_name']
#             db = connDb(database_type, ip_adress, user_name, user_pwd, db_name)
#             res = selectDB(db, sql, values)
#             logger = logging.getLogger(__name__)
#             logger.info(res.__next__())
if __name__ == "__main__":
    theMain()
    # theMain11()
