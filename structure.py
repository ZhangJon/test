#!usr/bin/env python
# -*- coding: utf-8 -*-


# ---数据库
import pymssql
import cx_Oracle
import pymysql
class DatabaseOperation(object):
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
# a = DatabaseOperation(**aaa)
# b = DatabaseOperation(**bbb)
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


# 加解密
import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
class AESCrypto(object):
    """AESCrypto."""

    def __init__(self, aes_key, aes_iv):
        """aes_key, aes_iv 可以自己定义，aes_key 32位，aes_iv 16位，如果用中文，一个中文字占三位"""
        if not isinstance(aes_key, bytes):
            aes_key = aes_key.encode()

        if not isinstance(aes_iv, bytes):
            aes_iv = aes_iv.encode()

        self.aes_key = aes_key
        self.aes_iv = aes_iv

    def encrypt(self, data, mode='cbc'):
        """encrypt."""
        func_name = '{}_encrypt'.format(mode)
        func = getattr(self, func_name)
        if not isinstance(data, bytes):
            data = data.encode()

        return func(data)

    def decrypt(self, data, mode='cbc'):
        """decrypt."""
        func_name = '{}_decrypt'.format(mode)
        func = getattr(self, func_name)

        if not isinstance(data, bytes):
            data = data.encode()

        return func(data)

    # def cfb_encrypt(self, data):
    #     """CFB encrypt."""
    #     cipher = Cipher(algorithms.AES(self.aes_key),
    #                     modes.CFB(self.aes_iv),
    #                     backend=default_backend())

    #     return cipher.encryptor().update(data)

    # def cfb_decrypt(self, data):
    #     """CFB decrypt."""
    #     cipher = Cipher(algorithms.AES(self.aes_key),
    #                     modes.CFB(self.aes_iv),
    #                     backend=default_backend())

    #     return cipher.decryptor().update(data)

    def ctr_encrypt(self, data):
        """ctr_encrypt."""
        cipher = Cipher(algorithms.AES(self.aes_key),
                        modes.CTR(self.aes_iv),
                        backend=default_backend())

        return cipher.encryptor().update(self.pkcs7_padding(data))

    def ctr_decrypt(self, data):
        """ctr_decrypt."""
        cipher = Cipher(algorithms.AES(self.aes_key),
                        modes.CTR(self.aes_iv),
                        backend=default_backend())

        uppaded_data = self.pkcs7_unpadding(cipher.decryptor().update(data))
        return uppaded_data.decode()

    def cbc_encrypt(self, data):
        """cbc_encrypt."""
        cipher = Cipher(algorithms.AES(self.aes_key),
                        modes.CBC(self.aes_iv),
                        backend=default_backend())

        return cipher.encryptor().update(self.pkcs7_padding(data))

    def cbc_decrypt(self, data):
        """cbc_decrypt."""
        cipher = Cipher(algorithms.AES(self.aes_key),
                        modes.CBC(self.aes_iv),
                        backend=default_backend())

        uppaded_data = self.pkcs7_unpadding(cipher.decryptor().update(data))
        return uppaded_data.decode()

    @staticmethod
    def pkcs7_padding(data):
        """pkcs7_padding."""
        padder = padding.PKCS7(algorithms.AES.block_size).padder()

        padded_data = padder.update(data) + padder.finalize()

        return padded_data

    @staticmethod
    def pkcs7_unpadding(padded_data):
        """pkcs7_unpadding."""
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data)

        try:
            uppadded_data = data + unpadder.finalize()
        except ValueError:
            raise ValueError('无效的加密信息!')
        else:
            return uppadded_data

# message = "QWERTYgfdsa12345！·#￥%"
# message = '123456'
message = 'LIS5152QRY'
# message = '\x82\x88\x10Q,\xfe\xdcS \xce\x9e\x95\x98,\xffP'
# crypto = AESCrypto('abcd1111abcd1111abcd1111abcd1111', 'abcd1111abcd1111')
crypto = AESCrypto('张-密^&($#@-7/*FK-ybf码w-学f', 'm2Vd=G进yt%爱&')
# crypto = AESCrypto('WDmG1e38igW53YuXkE0SsKUDeLbULAtL', 'm2VyHdx41zRgvg6f')
data1 = crypto.encrypt(message)

print(data1)
print(type(data1))

encodestr = str(base64.b64encode(data1),'utf-8')
print(encodestr)
print(type(encodestr))
decodestr = base64.b64decode(encodestr.encode('utf-8'))
print(decodestr)
data12 = crypto.decrypt(data1)
print(data12)