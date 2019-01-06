#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Jon Zhang 
@contact: zj.fly100@gmail.com
@site: 

@version: 1.0
@license: 
@file: 11111.py
@time: 2018-12-24 19:33

the line began to write the explanation and demonstration of this document
"""

import os,sys
import time
import datetime
import logging
import hashlib
import xml.etree.ElementTree as ET

import cx_Oracle
import MySQLdb
import pymssql


class XmlParse:
    def __init__(self, file_path):
        self.tree = None
        self.root = None
        self.xml_file_path = file_path

    def ReadXml(self):
        try:
            # print("xmlfile:", self.xml_file_path)
            self.tree = ET.parse(self.xml_file_path)
            self.root = self.tree.getroot()
        except Exception as e:
            print("parse xml faild!")
            sys.exit()
        else:
            pass
            # print("parse xml success!")
        finally:
            return self.tree


def LOGGER():
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)
    fh=logging.FileHandler('/tmp/match.log')
    ch=logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

    
def timmer(func):
    logger=LOGGER()
    def wrapper():
        start_time=datetime.datetime.now()
        func()
        stop_time=datetime.datetime.now()
        logger.info("运行时间%s"%(stop_time-start_time))
    return wrapper
    

def connDb(databasetype, ipAdress, listenPort, userName, userPwd, dbName):
    # dec = lambda t, n: ''.join([chr(ord(c) - n) for c in t])
    # userPwd = dec(userPwd,10)
    if databasetype == 'S':
        # print(ipAdress, userName, userPwd, dbName)
        conn = pymssql.connect(ipAdress, userName, userPwd, dbName)
        return conn
    elif databasetype == 'O':
        # print(ipAdress, listenPort, dbName,userName, userPwd)
        dsn = cx_Oracle.makedsn(ipAdress, listenPort, dbName)
        conn = cx_Oracle.connect(userName, userPwd, dsn)
        return conn
    elif databasetype == 'M':
        # print('M:',ipAdress, userName, userPwd, dbName)
        conn = MySQLdb.connect(ipAdress, userName, userPwd, dbName, charset='utf8')
        return conn

        
def selectDB(db, sql,result):
    logger = LOGGER()
    cursor = db.cursor()
    # print(sql)
    try:
        cursor.execute(sql)
    except Exception as e:
        #print(sql)
        logger.error(e)
    # results = cursor.fetchall()
    MatchingResults(cursor,result)
    cursor.close()
    db.close()
    

def MatchingResults(cur,result):
    logger=LOGGER()
    for i in cur:
        if result in str(i):
            logger.info("Match the result %s" %i)
            continue
        else:
            pass
            

def ReadMain(XML_NAME):
    logger=LOGGER()
    xml_file = os.path.abspath(XML_NAME)
    parse = XmlParse(xml_file)
    tree = parse.ReadXml()
    root = tree.getroot()
    logger.info(root)
    captionList = root.findall("EXCEL")  # 在当前指定目录下遍历
    # print(len(captionList))
    for caption in captionList:
        # print(caption.tag, "----", caption.attrib, "----", caption.text)
        child_list = caption.findall("SQL")
        dict_sheet_sql = {}
        for i in range(len(child_list)):
            # print(child_list[i].tag, "====", child_list[i].attrib, "====", child_list[i].text)
            # dcit_sheet_sql[str(i+1)] = [child_list[i].attrib['sheet_name'], child_list[i].text]
            dict_sheet_sql[child_list[i].attrib['sheet_name']] =  child_list[i].text
        # SELECT_SQL(nowTime,caption.attrib['EXCEL_NAME'],caption.attrib['EMAIL_ADD'],dcit_sheet_sql)
    
    return dict_sheet_sql

    
def main():
    databasetype = 'O'
    
    db = connDb(databasetype, ipAdress, listenPort, userName, userPwd, dbName)
    dict_sheet_sql = ReadMain(XML_NAME)
    for (k,v) in dict_sheet_sql:
        selectDB(db, v, k)
    

if __name__ == '__main__':
    main()