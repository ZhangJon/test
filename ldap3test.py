#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Jon Zhang 
@contact: zj.fly100@gmail.com
@site: 

@version: 1.0
@license: 
@file: ldap3test.py
@time: 2019-1-22 15:55

the line began to write the explanation and demonstration of this document
"""
from ldap3 import Server, Connection, ALL, SUBTREE, ServerPool
import os,json
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




LDAP_SERVER_POOL = ["110.100.16.199"]
LDAP_SERVER_PORT = 389
ADMIN_DN = "p000801101@testdomain.com.cn"
ADMIN_PASSWORD = "Wa33Wa33"
SEARCH_BASE = 'OU=Citrix DC=testdomain,DC=com,DC=cn'
SetupLogging(default_path='logging.json', default_level=logging.debug, env_key='LOG_CFG')
logger = logging.getLogger(__name__)

def ldap_auth(username, password):
    ldap_server_pool = ServerPool(LDAP_SERVER_POOL)
    conn = Connection(ldap_server_pool, user=ADMIN_DN, password=ADMIN_PASSWORD, check_names=True, lazy=False, raise_exceptions=False)
    conn.open()
    conn.bind()

    res = conn.search(
        search_base = SEARCH_BASE,
        search_filter = '(sAMAccountName={})'.format(username),
        search_scope = SUBTREE,
        attributes = ['cn', 'givenName', 'mail', 'sAMAccountName'],
        paged_size = 5
    )

    if res:
        entry = conn.response[0]
        dn = entry['dn']
        attr_dict = entry['attributes']

        # check password by dn
        try:
            conn2 = Connection(ldap_server_pool, user=dn, password=password, check_names=True, lazy=False, raise_exceptions=False)
            conn2.bind()
            if conn2.result["description"] == "success":
                logger.info((True, attr_dict["mail"], attr_dict["sAMAccountName"], attr_dict["givenName"]))
                return (True, attr_dict["mail"], attr_dict["sAMAccountName"], attr_dict["givenName"])
            else:
                logger.info("auth fail")
                return (False, None, None, None)
        except Exception as e:
            logger.info("auth fail")
            return (False, None, None, None)
    else:
        return (False, None, None, None)


if __name__ == "__main__":
    ldap_auth("p000801101", "Wa33Wa33")
