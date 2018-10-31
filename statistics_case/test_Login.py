# -*- coding: utf-8 -*-
# @Time    : 11:50
# @Author  : Administor
# @File    : test_Login.py
# @Software: PyCharm

import unittest
from config.readConfig import read_config
import requests
import json
from log.logger import Logger
from common.common import *

logger = Logger(logger='statistics_case').getlog()

class test_Login(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass

    s = requests.session()
    '''
     @Description:传入相关的环境，返回不同的token，以供使用
    '''
    def test_login(self,inver):
        token = ''
        if inver == 'pre_online':
            url = read_config().get_string('pre_online','login')
            r = self.s.post(
                url,
                json={"mobile": "18399917685","password":"~~~aibilizh"}
            )
            status_code = r.status_code
            if status_code == 200:
                json_dict = json.loads(r.text)
                if type(json_dict).__name__ == 'dict':
                    token = json_dict['data']['token']
            else:
                print("接口登录失败")
        elif inver == 'test':
            url = read_config().get_string('test','login')
            t = self.s.post(
                url,
                json={"mobile": "18399917685", "password": "zh0514"}
            )
            statusCode = t.status_code
            if statusCode == 200 :
                json_dict_t = json.loads(t.text)
                if type(json_dict_t).__name__ == 'dict':
                    token = json_dict_t['data']['token']
            else:
                print("接口登录失败")
        elif inver == 'pre_h5':
            url = read_config().get_string('pre_h5', 'login')
            v = self.s.post(
                url,
                json={"mobile": "13139236776","password":"123456","timestamp": "1540371932711"}
            )
            code = v.status_code
            if code == 200 :
                json_dict_v = json.loads(v.text)
                if type(json_dict_v).__name__ == 'dict':
                    token = json_dict_v['data']['token']
            else:
                print("接口登录失败")
        return token

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')