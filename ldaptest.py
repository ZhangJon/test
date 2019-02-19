#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Jon Zhang 
@contact: zj.fly100@gmail.com
@site: 

@version: 1.0
@license: 
@file: ldaptest.py
@time: 2019-1-22 14:29

the line began to write the explanation and demonstration of this document
"""
# -*- coding: UTF-8 -*-
import sys
import os
import json
import ldap
import ldap
import logging
import logging.config
import time


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


class ldapc:
    def __init__(self, ldap_path, baseDN, ldap_authuser, ldap_authpass):
        SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
        self.logger = logging.getLogger(__name__)
        self.baseDN = baseDN
        self.ldap_error = None
        self.l = ldap.initialize(ldap_path)
        self.l.protocol_version = ldap.VERSION3
        self.logger.debug('url:%s' %ldap_path)
        self.logger.debug('username:%s' %ldap_authuser)
        self.logger.debug('password:%s' %ldap_authpass)
        try:
            res = self.l.simple_bind_s(ldap_authuser, ldap_authpass)
            self.logger.debug(res)
        except ldap.ldapError as err:
            self.ldap_error = 'Connect to %s failed, Error:%s.' % (ldap_path, err.message['desc'])
            self.logger.error(self.ldap_error)
        # finally:
        #     self.l.unbind_s()
        #     del self.l

    def search_users(self, username):  # 模糊查找，返回一个list，使用search_s()
        if self.ldap_error is None:
            try:
                searchScope = ldap.SCOPE_SUBTREE
                searchFiltername = "sAMAccountName"  # 通过samaccountname查找用户
                retrieveAttributes = None
                searchFilter = '(' + searchFiltername + "=" + username + '*)'
                ldap_result = self.l.search_s(self.baseDN, searchScope, searchFilter, retrieveAttributes)
                if len(ldap_result) == 0:  # ldap_result is a list.
                    return "%s doesn't exist." % username
                else:
                    # result_type, result_data = self.l.result(ldap_result, 0)
                    # return result_type, ldap_result
                    return ldap_result
            except ldap.ldapError as err:
                return err

    def search_user(self, username):  # 精确查找，返回值为list，使用search()
        if self.ldap_error is None:
            try:
                searchScope = ldap.SCOPE_SUBTREE
                searchFiltername = "sAMAccountName"  # 通过samaccountname查找用户
                retrieveAttributes = None
                searchFilter = '(' + searchFiltername + "=" + username + ')'
                ldap_result_id = self.l.search(self.baseDN, searchScope, searchFilter, retrieveAttributes)
                result_type, result_data = self.l.result(ldap_result_id, 0)
                if result_type == ldap.RES_SEARCH_ENTRY:
                    return result_data
                else:
                    return "%s doesn't exist." % username
            except ldap.ldapError as err:
                return err

    def search_userDN(self, username):  # 精确查找，最后返回该用户的DN值
        if self.ldap_error is None:
            try:
                searchScope = ldap.SCOPE_SUBTREE
                searchFiltername = "sAMAccountName"  # 通过samaccountname查找用户
                retrieveAttributes = None
                searchFilter = '(' + searchFiltername + "=" + username + ')'
                ldap_result_id = self.l.search(self.baseDN, searchScope, searchFilter, retrieveAttributes)
                result_type, result_data = self.l.result(ldap_result_id, 0)
                if result_type == ldap.RES_SEARCH_ENTRY:
                    self.logger.debug('flag:1')
                    return result_data[0][0]  # list第一个值为用户的DN，第二个值是一个dict，包含了用户属性信息
                else:
                    self.logger.debug('flag:0')
                    return "%s doesn't exist." % username
            except ldap.ldapError as err:
                return err

    def valid_user(self, username, userpassword):  # 验证用户密码是否正确
        if self.ldap_error is None:
            target_user = self.search_userDN(username)  # 使用前面定义的search_userDN函数获取用户的DN
            if target_user.find("doesn't exist") == -1:
                try:
                    self.l.simple_bind_s(target_user, userpassword)
                    self.logger.info('%s valid passed.\r' % (username))  # logging会自动在每行log后面添加"\000"换行，windows下未自动换行
                    return True
                except ldap.ldapError as err:
                    return err
            else:
                return target_user

    def update_pass(self, username, oldpassword, newpassword):  #####未测试#########
        if self.ldap_error is None:
            target_user = self.search_userDN(username)
            if target_user.find("doesn't exist") == -1:
                try:
                    self.l.simple_bind_s(target_user, oldpassword)
                    self.l.passwd_s(target_user, oldpassword, newpassword)
                    return 'Change password success.'
                except ldap.ldapError as err:
                    return err
            else:
                return target_user


ldap_authuser = 'p000801101'
ldap_authpass = 'Wa33Wa33'
domainname = 'testdomain.com.cn'
ldappath = 'ldap://10.100.16.199:389'

baseDN = 'DC=testdomain,DC=com,DC=cn'  # ldap_authuser在连接到ldap的时候不会用到baseDN，在验证其他用户的时候才需要使用
username = 'p000801101'  # 要查找/验证的用户
p = ldapc(ldappath, baseDN, ldap_authuser, ldap_authpass)
# print 'list--search:',p.search_users(username)
print('DN----search', p.search_userDN(username))
print('DN-ty', type(p.search_userDN(username)))
print('user--valid', p.valid_user(ldap_authuser, ldap_authpass))  # 调用valid_user()方法验证用户是否为合法用户

# OU=Citrix OU=CTXUsers OU=PVS