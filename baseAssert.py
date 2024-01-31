#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from mylog import logger


class BaseAssert(object):
    """
    断言信息封装
    """

    def __init__(self, newpoco):
        self.newpoco = newpoco
        self.log = logger()

    def assert_exist_element(self, element):
        self.log.info(f'断言：存在元素 {element}')
        self.newpoco(element).wait_for_appearance()
        self.newpoco(element).exists()

    def assert_exist_btnSelect(self):
        self.assert_exist_element('btnSelect')

    def assert_exist_btnJump(self):
        self.assert_exist_element('btnJump')

    def assert_exist_btnGo(self):
        self.assert_exist_element('btnGo')
