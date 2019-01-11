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


import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')



pc = prpcrypt('keyskeyskeyskeys')  # 初始化密钥
e = pc.encrypt("00000")
d = pc.decrypt(e)
print
e, d
e = pc.encrypt("00000000000000000000000000")
d = pc.decrypt(e)
print
e, d
