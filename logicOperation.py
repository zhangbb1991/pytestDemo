#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import re

from airtest.core.api import *
from mylog import logger
from baseOperation import BaseOperation, BaseGetNodeInfo
#from page.main.mansion.mansionPage import MansionPage
from mainPage import MainPage


class Logicoperation(object):
    """
    业务逻辑或计算逻辑封装
    """

    def __init__(self, newpoco):
        self.newpoco = newpoco
        self.log = logger()
        self.base = BaseOperation(newpoco)
        self.baseInfo = BaseGetNodeInfo(newpoco)
        #self.mansionPage = MansionPage(newpoco)
        self.mainPage = MainPage(newpoco)

    def calcuate_option_cnt(self, ret):
        """
        :param ret: 文本，如 0/1
        :return: 操作次数
        """
        self.log.info(f'{ret}')
        numbers = re.findall(r'\d+', ret)
        cnt = int(numbers[1]) - int(numbers[0])
        self.log.info(f'计算出来的操作次数： {cnt}')
        return cnt

    # 多次调用函数
    def __execute_function_n_times(self, func, n=None):
        ret = self.baseInfo.get_task_txt_condition()
        n = self.calcuate_option_cnt(ret)
        for i in range(n):
            func()

    def __assert_exist_and_click(self, locator):
        time.sleep(1)
        if self.newpoco(locator).exists():
            self.newpoco(locator).click()
            time.sleep(1)

    def click_get_times(self, n):
        """
        点击 招募N次
        :return:
        """
        for i in range(n):
            self.base.click_get()
            time.sleep(1)

    def click_attack_idx_times(self, idx, n):
        """乔迁风云：收购N次"""
        for i in range(n):
            self.base.click_attack_idx(idx)
            time.sleep(1)

    def click_lab_tips_times(self):
        """
        点击 点击继续，直到不再出现该对话框
        :return:
        """
        while True:
            if self.newpoco('dialogPanel').exists():
                # time.sleep(2)
                self.base.click_lab_tips()
            else:
                break

    def click_trade_times(self, cnt):
        """
        点击N次贸易
        :param cnt:
        :return:
        """
        for i in range(cnt):
            self.base.click_trade()
            time.sleep(0.5)

    def get_number_from_string(self, input_text):
        """
        从提示文本中提取数字，用于处理 如 门客升级和门客技能提升的场景
        :param input_text:如 1名門客達到10級，提取 1、10
        :return: 返回数组
        """
        numbers = re.findall(r'\d+', input_text)
        for i in range(len(numbers)):
            numbers[i] = int(numbers[i])
        return numbers

    def assert_and_click_go(self):
        """如果出现btnGo,则点击btnGo"""
        self.__assert_exist_and_click('btnGo')

    def assert_and_click_confirm(self):
        """如果出现btnConfirm,则点击btnConfirm"""
        self.__assert_exist_and_click('btnConfirm')

    def assert_and_click_cancel(self):
        """如果出现btnCancel,则点击btnCancel"""
        self.__assert_exist_and_click('btnCancel')

    def assert_and_click_cancel1(self):
        """如果出现btnCancel,则点击btnCancel1"""
        self.__assert_exist_and_click('btnCancel1')

    def assert_and_click_acqiure(self):
        """如果出现Acquire,则点击Acquire(获得珍兽)"""
        self.__assert_exist_and_click('Acquire')

    def assert_task_finish(self):
        """断言任务完成（读取主线任务的condition来计算并判断）"""
        ret = self.mainPage.get_task_txt_condition()
        cnt = self.calcuate_option_cnt(ret)
        assert cnt == 0

    def assert_offline_benefits_and_click_confirm(self):
        """断言出现 离线收益，点击空白处关闭"""
        if self.newpoco('spineCom').exists():
            self.base.click_confirm()
            time.sleep(0.5)

    def assert_weekly_card_pop_view_and_click_empty(self):
        """断言出现 特权周卡，点击空白处关闭"""
        if self.newpoco('WeeklyCardPopView').exists():
            self.base.click_empty()
