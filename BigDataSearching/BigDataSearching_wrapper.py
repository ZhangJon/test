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
import threading
################################
import pymssql
import cx_Oracle
import pymysql
import threadpool


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


def connDb(**kwargs):
    database_type = kwargs['database_type']
    ip_adress = kwargs['ip_adress']
    user_name = kwargs['user_name']
    user_pwd = kwargs['user_pwd']
    db_name = kwargs['db_name']
    listen_port = kwargs['listen_port']
    if database_type == 'O':
        dsn = cx_Oracle.makedsn(ip_adress, listen_port, db_name)
        conn = cx_Oracle.connect(user_name, user_pwd, dsn)
        return conn
    if database_type == 'S':
        conn = pymssql.connect(ip_adress, user_name, user_pwd, db_name)
        return conn
    if database_type == 'M':
        conn = pymysql.connect(ip_adress, user_name, user_pwd, db_name, charset='utf8')
        return conn


def selectDB(**kwargs):
    db = kwargs['db']
    sql = kwargs['sql']
    values = kwargs['values']
    setup_logging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
    logger = logging.getLogger(__name__)
    cursor = db.cursor()
    cursor.execute(sql)
    for result in cursor:
        logger.debug(result)
        logger.debug(values)
        if values in str(result):
            cursor.close()
            db.close()
            return result
        else:
            pass
    cursor.close()
    db.close()
    return False


def timeer(func):
    def wrapper():
        setup_logging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
        logger = logging.getLogger(__name__)
        a = datetime.datetime.now()
        func()
        b = datetime.datetime.now()
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
        child_list = caption.findall("body")
        list_dict_str = []
        logger.debug(child_list)
        for i in range(len(child_list)):
            dict_str = {}
            dict_str[child_list[i].attrib['match_str']] = child_list[i].text
            list_dict_str.append(dict_str)
        logger.debug('list_dict_str--->%s' % list_dict_str)
        dict_all_list[dict_db_list['type']] = [dict_db_list, list_dict_str]
    logger.info(dict_all_list)
    return dict_all_list


@timeer
def theMain():
    setup_logging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
    logger = logging.getLogger(__name__)
    dict_all_list = ReadMain('EXP_DATA_CONF.xml')
    for i in range(len(dict_all_list.keys())):
        dict_db_list, list_dict_str = dict_all_list[list(dict_all_list.keys())[i]]
        codes = []
        for i in list_dict_str:
            lists = {}
            logger.debug(i)
            values = list(i.keys())[0]
            sql = i[values]
            # database_type = dict_db_list['database_type']
            # ip_adress = dict_db_list['ip_adress']
            # user_name = dict_db_list['user_name']
            # user_pwd = dict_db_list['user_pwd']
            # db_name = dict_db_list['db_name']
            # listen_port = dict_db_list['listen_port']
            # db = connDb(database_type, ip_adress, user_name, user_pwd, db_name, listen_port)
            db = connDb(**dict_db_list)
            lists['db'] = db
            lists['sql'] = sql
            lists['values'] = values
            codes.append(lists)
            # res = selectDB(lists)
            # logger.info(res)

        # 多线程方式1
        # logger.debug(codes)
        # pool = threadpool.ThreadPool(2)
        # tasks = threadpool.makeRequests(selectDB,codes)
        # [pool.putRequest(task) for task in tasks]
        # pool.wait()

        # 多线程方式2
        logger.debug(codes)
        threads = []
        files = range(len(codes))
        for i in codes:
            t = threading.Thread(target=selectDB,kwargs=i)
            threads.append(t)

        for j in files:
            threads[j].start()
        for j in files:
            threads[j].join()



if __name__ == "__main__":
    theMain()
