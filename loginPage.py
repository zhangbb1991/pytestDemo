#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from airtest.core.api import *
from mylog import logger


class LoginPage(object):
    """登录"""

    def __init__(self, newpoco):
        self.newpoco = newpoco
        self.log = logger()

    def __click_button(self, locator):
        self.newpoco(locator).wait_for_appearance()
        self.newpoco(locator).click()

    def clear_input_text(self, locator):
        """清空输入框文本"""
        current_text = self.newpoco(locator).get_text()
        for char in current_text:
            keyevent('KEYCODE_DEL')

    def swipeItem(self, locator):
        """滑动窗口"""
        self.log.info('滑动窗口')
        list_height = self.newpoco(locator).get_position()[1] + self.newpoco(locator).get_size()[1]
        start_point = [0.5, 0.5]
        end_point = [0.5, list_height / self.newpoco.get_screen_size()[1]]
        self.newpoco.swipe(start_point, end_point)

    def click_input_text(self):
        """点击 文本输入框"""
        self.log.info('点击 输入账号')
        self.__click_button('txtAccountInput')

    def click_change(self):
        """点击 换区"""
        self.__click_button('btnChange')

    def select_server(self, server):
        """选择 测试服"""
        self.newpoco(text=server).click()

    def select_area(self, area):
        """选择 区服"""
        self.newpoco(text=area).click()

    def swipe_server(self):
        """向下滑动 测试服"""
        self.swipeItem('TabItem')

    def swipe_area(self):
        """向下滑动 区服"""
        self.swipeItem('ServerItem')

    def click_start(self):
        """点击 开始游戏"""
        self.log.info('点击 开始游戏')
        self.__click_button('btnStart')
