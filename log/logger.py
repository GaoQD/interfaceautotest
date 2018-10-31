# -*- coding: utf-8 -*-
# @Time    : 11:17
# @Author  : Administor
# @File    : logger.py
# @Software: PyCharm

import logging
import os.path

'''
 @Description:获取日志文件以及写入日志
'''
class Logger(object):
    def __init__(self,logger):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        log_path = os.path.dirname(os.path.abspath('.')) + '\\log\\'
        log_name = log_path + 'test.log'

        filehandle = logging.FileHandler(log_name,encoding='utf-8')
        filehandle.setLevel(logging.INFO)

        controlhandle = logging.StreamHandler()
        controlhandle.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')
        filehandle.setFormatter(formatter)
        controlhandle.setFormatter(formatter)

        self.logger.addHandler(filehandle)
        self.logger.addHandler(controlhandle)

    def getlog(self):
        return self.logger