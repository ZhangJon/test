#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Jon Zhang 
@contact: zj.fly100@gmail.com
@site: 

@version: 1.0
@license: 
@file: TEST_XML.py
@time: 2018-12-27 16:50

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
# import pymssql
import cx_Oracle
import pymysql


def SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG'):
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


def ConnDb(database_type, ip_adress, user_name, user_pwd, db_name, listen_port=None):
    if database_type == 'O':
        dsn = cx_Oracle.makedsn(ip_adress, listen_port, db_name)
        conn = cx_Oracle.connect(user_name, user_pwd, dsn)
        return conn
    elif database_type == 'M':
        conn = pymysql.connect(ip_adress, user_name, user_pwd, db_name, charset='utf8')
        return conn
    # elif database_type == 'S':
    #     conn = pymssql.connect(ip_adress, user_name, user_pwd, db_name)
    #     return conn


def SelectDB(db, sql):
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor


def MatchStr(cur,db,values):
    for result in cur:
        if values in str(result):
            cur.close()
            db.close()
            yield True, result
        else:
            cur.close()
            db.close()
            yield False


def SpellSql(cur, db, user):
    results = cur.fetchall()
    cur.close()
    db.close()
    res = []
    for result in results:
        result = "select * from %s.%s" %(user, result[0])
        # result = "select * from %s" %(result)
        # yield result
        res.append(result)
    return res


class XmlParse(object):
    def __init__(self, file_path):
        self.tree = None
        self.root = None
        self.xml_file_path = file_path
        SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
        self.logger = logger = logging.getLogger(__name__)

    def ReadXml(self):
        try:
            self.logger.info("xmlfile: %s" %self.xml_file_path)
            self.tree = ET.parse(self.xml_file_path)
            self.root = self.tree.getroot()
        except Exception as e:
            self.logger.info("parse xml faild!")
            sys.exit()
        else:
            pass
            self.logger.info("parse xml success!")
        finally:
            return self.tree

    def CreateNode(self, tag, attrib, text):
        element = ET.Element(tag, attrib)
        element.text = text
        self.logger.debug("tag:%s;attrib:%s;text:%s" % (tag, attrib, text))
        return element

    def AddNode(self, Parent, tag, attrib, text):
        element = self.CreateNode(tag, attrib, text)
        self.logger.debug(Parent)
        # if Parent:
        #     print(Parent)
        #     Parent.append(element)
        #     el = self.root.find('Head')
        #     self.logger.debug( "%s----%s----%s" %(el.tag, el.attrib, el.text))
        # else:
        #     self.logger.debug("parent is none")

        Parent.append(element)
        el = self.root.find('Head')
        self.logger.debug( "%s----%s----%s" %(el.tag, el.attrib, el.text))


    def WriteXml(self, destfile):
        dest_xml_file = os.path.abspath(destfile)
        self.tree.write(dest_xml_file, encoding="utf-8", xml_declaration=True)


def MainText():
    SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
    logger = logging.getLogger(__name__)
    flag_staus = True
    while flag_staus:
        match_str = input("Please input your match str>>").strip()
        # xml_nam = input("Please input your config name>>").strip()
        if match_str:
            # xml_name = "%s.xml" %xml_nam
            xml_name = "test.xml"
            logger.info(xml_name)
            xml_file = os.path.abspath(xml_name)
            parses = XmlParse(xml_file)
            tree = parses.ReadXml()
            root = tree.getroot()
            captionList = root.findall("Head")
            logger.debug(root)
            logger.debug(captionList)
            for caption in captionList:
                dict_db_list = caption.attrib
                logger.debug(caption)
                database_type = dict_db_list['database_type']
                ip_adress = dict_db_list['ip_adress']
                user_name = dict_db_list['user_name']
                user_pwd = dict_db_list['user_pwd']
                db_name = dict_db_list['db_name']
                listen_port = dict_db_list['listen_port']
                sql = dict_db_list['sql']
                db = ConnDb(database_type, ip_adress, user_name, user_pwd, db_name, listen_port)
                cur = SelectDB(db, sql)
                result = SpellSql(cur, db, db_name)
                logger.debug(result)
                # parses.AddNode(caption, "body", {"match_str": "22"}, result.__next__())
                for ret in result:
                    parses.AddNode(caption, "body", {"match_str": match_str}, ret)
            # new_xml = "%s_%s.xml" %(xml_nam,match_str)
            new_xml = "test_%s.xml" %(match_str)
            parses.WriteXml(new_xml)
            flag_staus = False
        else:continue



if __name__ == "__main__":
    MainText()
