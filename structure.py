# ---数据库
import pymssql
import cx_Oracle
import pymysql
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


# aaa = {'database_type': 'M', 'db_name': 'oldboy', 'ip_adress': '10.73.62.217', 'listen_port': '3306', 'user_name': 'root', 'user_pwd': '123456' ,'values':'5','sql': 'select * from oldboy.student'}
# bbb = {'database_type': 'M', 'db_name': 'oldboy', 'ip_adress': '10.73.62.217', 'listen_port': '3307', 'user_name': 'root', 'user_pwd': '123456' ,'values':'777777','sql': 'select * from oldboy.student01'}
#
# a = DatabaseOpertion(**aaa)
# b = DatabaseOpertion(**bbb)
#
# aa = a.SelectDatabase()
# print(aa)
# bb = b.SelectDatabase()
# print(bb)



#--配置文件
import sys
import xml.etree.ElementTree as ET
class XmlParse(object):
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
            print("parse xml success!")
        finally:
            return self.tree

    def WriteXml(self):
        pass



