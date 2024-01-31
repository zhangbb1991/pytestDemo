#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from mylog import logger


class MainPage:
    """游戏主页"""

    def __init__(self, newpoco):
        self.newpoco = newpoco
        self.log = logger()

    def click_btn_home(self, idx):
        """点击 Home栏"""
        locator = 'btnHome' + str(idx)
        self.newpoco(locator).click()

    # idx=1:府邸 idx=2 商铺 idx=3:门客 idx=4:关卡 idx=5:城郊 idx=6:背包

    def click_mansion(self):
        """点击 府邸"""
        self.log.info('点击 府邸')
        self.click_btn_home(1)

    def click_market(self):
        """点击 商铺"""
        self.log.info('点击 商铺')
        self.click_btn_home(2)

    def click_retainer(self):
        """点击 门客"""
        self.log.info('点击 门客')
        self.click_btn_home(3)

    def click_stage(self):
        """点击 关卡"""
        self.log.info('点击 关卡')
        self.click_btn_home(4)

    def click_adventure(self):
        """点击 闯荡"""
        self.log.info('点击 闯荡')
        #self.click_btn_home(4_1)
        self.newpoco('btnHome4_1').click()

    def click_suburb(self):
        """点击 城郊"""
        self.log.info('点击 城郊')
        self.click_btn_home(5)

    def click_bag(self):
        """点击 背包"""
        self.log.info('点击 背包')
        self.click_btn_home(6)

    def click_headicon(self):
        """点击 头像（左上角的身份头像）"""
        self.log.info('点击 身份头像')
        self.newpoco('headIconItem').wait_for_appearance()
        self.newpoco('headIconItem').click()

    def get_task_txt_condition(self):
        """
        :return: 获取主线任务的条件，用于计算需要操作的次数
        """
        self.log.info('获取主线任务的条件')
        ret = self.newpoco('taskItem').offspring('taskTxtCondition').get_text()
        self.log.info(f'获取到的条件：{ret}')
        return ret

    def get_task_txt_name(self):
        """
        :return: 获取主线任务的文本
        """
        self.log.info('获取主线任务的文本')
        ret = self.newpoco('taskItem').offspring('taskTxtName').get_text()
        self.log.info(f'获取到的文本：{ret}')
        return ret
