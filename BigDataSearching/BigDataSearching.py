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
import datetime

import pymssql
import cx_Oracle
import MySQLdb

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
    # print(cursor)
    for result in cursor:
        if values in str(result):
            cursor.close()
            db.close()
            yield True,result
        else:
            cursor.close()
            db.close()
            yield False




def selectDB11(db, sql, values):
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(cursor)
    for result in results:
        if values in str(result):
            cursor.close()
            db.close()
            yield True, result
        else:
            cursor.close()
            db.close()
            yield False



def theMain():
    sql = """select * from city"""
    values = '20180000000'
    database_type = 'M'
    ip_adress = '127.0.0.1'
    user_name = 'root'
    user_pwd = 'oracle'
    db_name = 'world'
    db = connDb(database_type, ip_adress, user_name, user_pwd, db_name)
    print(selectDB(db, sql, values))


def theMain11():
    sql = """select * from city"""
    values = '20180000000'
    database_type = 'M'
    ip_adress = '127.0.0.1'
    user_name = 'root'
    user_pwd = 'oracle'
    db_name = 'world'
    db = connDb(database_type, ip_adress, user_name, user_pwd, db_name)
    print(selectDB11(db, sql, values))


if __name__ == "__main__":
    a=datetime.datetime.now()
    theMain()
    b=datetime.datetime.now()
    print("Curson使用时间：",b-a)

    c=datetime.datetime.now()
    theMain11()
    d=datetime.datetime.now()
    print("fetchall使用时间：",d-c)

