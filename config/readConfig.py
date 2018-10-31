# -*- coding: utf-8 -*-
# @Time    : 11:07
# @Author  : Administor
# @File    : readConfig.py
# @Software: PyCharm
import configparser
import os

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir,'cfg.ini')

'''
 @Description:读取ini文件内容
'''
class read_config:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath,encoding='utf-8')

    def get_sections(self):
        if self.cf:
            return self.cf.sections()

    def get_sections_item(self,section):
        if self.cf:
            return self.cf.items(section)

    def get_string(self,section,option):
        if self.cf:
            return self.cf.get(section,option)

    def get_int(self,section,option):
        if self.cf:
            return self.cf.getint(section,option)

    def get_float(self,section,option):
        if self.cf:
            return self.cf.getfloat(section,option)

    def get_boolean(self,section,option):
        if self.cf:
            return self.cf.getboolean(section,option)