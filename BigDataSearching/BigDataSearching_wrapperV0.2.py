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

import cx_Oracle


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


class XmlParse(object):
    def __init__(self, file_path):
        self.tree = None
        self.root = None
        self.xml_file_path = file_path
        SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
        self.logger = logging.getLogger(__name__)

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


def ConnDb(database_type, ip_adress, user_name, user_pwd, db_name, listen_port=None):
    if database_type == 'O':
        dsn = cx_Oracle.makedsn(ip_adress, listen_port, db_name)
        conn = cx_Oracle.connect(user_name, user_pwd, dsn)
        return conn


def SelectDB(db, sql):
    SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
    logger = logging.getLogger(__name__)
    cursor = db.cursor()
    logger.info(sql)
    cursor.execute(sql)
    return cursor


def MatchStr(cur,db,values):
    SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
    logger = logging.getLogger(__name__)
    for result in cur:
        logger.debug(result)
        if values in str(result):
            cur.close()
            db.close()
            yield "[%s]匹配成功:%s" %(values,result)
    else:
        cur.close()
        db.close()
        yield "[%s]未匹配成功" %values


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


def timeer(func):
    def wrapper(*args, **kwargs):
        SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
        logger = logging.getLogger(__name__)
        a = datetime.datetime.now()
        func(*args, **kwargs)
        b = datetime.datetime.now()
        logger.debug("使用时间：%s" % (b - a))
    return wrapper


def ReadMain(XML_NAME):
    SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
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
    return dict_all_list


class DatabaseOpertion(object):
    def __init__(self,*args,**kwargs):
        self.conn = None
        self.cursor = None
        self.args = args
        self.kwargs = kwargs

    def ConnDatabase(self):
        database_type = self.kwargs['database_type']
        ip_adress = self.kwargs['ip_adress']
        user_name = self.kwargs['user_name']
        user_pwd = self.kwargs['user_pwd']
        db_name = self.kwargs['db_name']
        listen_port = self.kwargs['listen_port']
        if database_type == 'O':
            dsn = cx_Oracle.makedsn(ip_adress, listen_port, db_name)
            self.conn = cx_Oracle.connect(user_name, user_pwd, dsn)
            return self.conn
        elif database_type == 'S':
            self.conn = pymssql.connect(ip_adress, user_name, user_pwd, db_name)
            return self.conn
        elif database_type == 'M':
            self.conn = pymysql.connect(ip_adress, user_name, user_pwd, db_name, charset='utf8')
            return self.conn

    def SelectDatabase(self):
        sql = self.kwargs['sql']
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        return self.cursor

    def UpdateDatabase(self):
        pass

    def DeleteDatabase(self):
        pass

    def MatchStr(self):
        self.SelectDatabase()
        values = self.kwargs['values']
        for result in self.cursor:
            if values in str(result):
                self.cursor.close()
                self.conn.close()
                return result
            else:
                pass
        self.cursor.close()
        self.conn.close()
        return False

    def PieceTogetherSql(self):
        self.SelectDatabase()
        database_type = self.kwargs['database_type']
        results = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        res = []
        if database_type == 'O':
            user_name = self.kwargs['user_name']
            for result in results:
                result = "select * from %s.%s" % (user_name,result[0])
                res.append(result)
        elif database_type == 'S':
            for result in results:
                result = "select * from %s" % (result[0])
                res.append(result)
        elif database_type == 'M':
            db_name = self.kwargs['db_name']
            for result in results:
                result = "select * from %s.%s" % (db_name,result[0])
                res.append(result)
        return res


@timeer
def theMain(xml_file):
    SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
    logger = logging.getLogger(__name__)
    logger.debug(xml_file)
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    dict_all_list = ReadMain(xml_file)
    logger.debug(dict_all_list)
    for i in range(len(dict_all_list.keys())):
        logger.debug(i)
        dict_db_list, list_dict_str = dict_all_list[list(dict_all_list.keys())[i]]
        logger.debug(dict_db_list)
        logger.debug(list_dict_str)
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
            db = ConnDb(database_type, ip_adress, user_name, user_pwd, db_name, listen_port)
            res = SelectDB(db, sql)
            ret = MatchStr(res, db, values)
            logger.info(ret.__next__())


def MainText():
    SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
    logger = logging.getLogger(__name__)
    flag_staus = True
    while flag_staus:
        match_strs = input("Please input your match str>>").strip().split(",")
        logger.debug(match_strs)
        xml_nam = input("Please input your config name>>").strip()
        # if match_strs:
        if xml_nam:
            xml_name = "%s.xml" %xml_nam
            for match_str in match_strs:
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
                    result = SpellSql(cur, db, user_name)
                    logger.debug(result)
                    # parses.AddNode(caption, "body", {"match_str": "22"}, result.__next__())
                    for ret in result:
                        parses.AddNode(caption, "body", {"match_str": match_str}, ret)
                # new_xml = "%s_%s.xml" %(xml_nam,match_str)
                new_xml = "test_%s.xml" %(match_str)
                parses.WriteXml(new_xml)
                yield new_xml
            flag_staus = False
        else:continue
    # return (new_xml)


if __name__ == "__main__":
    new_xml = MainText()
    # print(new_xml)
    for i in new_xml:
        theMain(i)
