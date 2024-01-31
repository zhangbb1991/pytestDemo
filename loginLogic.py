#!/usr/bin/env python 
# -*- coding:utf-8 -*-

from baseOperation import BaseOperation
from baseAssert import BaseAssert
from loginPage import LoginPage
from logicOperation import Logicoperation
from airtest.core.api import *
from mylog import logger
from myAirtest import myAirTest


class LoginLogic(object):

	def __init__(self, newpoco):
		self.loginPage = LoginPage(newpoco)
		self.base = BaseOperation(newpoco)
		self.bassert = BaseAssert(newpoco)
		self.log = logger()
		self.newpoco = newpoco
		self.myAirTest = myAirTest()

	def input_account_text(self, account):
		"""清空输入框，输入测试账号"""
		if self.newpoco('txtAccountInput').get_text() != account:
			self.log.info('点击账号输入框')
			self.loginPage.click_input_text()
			# 清空输入框内容
			self.loginPage.clear_input_text('txtAccountInput')
			self.log.info('输入账号')
			text(account)
			self.log.info(f'输入的账号是：{account}')
		else:
			print(f'当前账号和测试账号{account}相同，无需输入！')


	def select_game_server(self):
		"""选择游戏服"""
		server = self.myAirTest.readIniConf('common', 'game_server')
		area = self.myAirTest.readIniConf('common', 'game_area')
		self.log.info(f'测试服： {server}   {area}')
		current_area = self.newpoco('txtSelected').get_text()
		self.log.info(f'当前服： {current_area}')
		if current_area != area:
			# 点击 换区
			self.loginPage.click_change()
			time.sleep(0.5)
			# 向下滑动 选择 服务组
			self.newpoco.swipe([0.179, 0.545], [0.179, 0.102])
			time.sleep(2)
			self.loginPage.select_server(server)
			"""
			while True:
				if not self.newpoco('txtState2', text=server).exists(): # todo 这里总是True
					self.newpoco.swipe([0.179, 0.545], [0.179, 0.302])
					time.sleep(0.5)
				else:
					self.loginPage.select_server(server)
					break
			"""
			# 向下滑动 选择 区服
			time.sleep(0.5)
			for i in range(7):
				self.newpoco.swipe([0.552, 0.609], [0.552, 0.271])
			time.sleep(1)
			self.loginPage.select_area(area)
			"""
			while True:
				print(self.newpoco(text=area).exists())
				if not self.newpoco(text=area).exists():

					self.newpoco.swipe([0.552, 0.609], [0.552, 0.271])
					time.sleep(0.5)
				else:
					self.loginPage.select_area(area)
					self.log.info('区域选择成功')
					break
				"""
		time.sleep(1)

	def login_game(self, account):
		"""直接登录游戏"""
		# 输入账号
		self.input_account_text(account)
		# 如果不是期望测试服，则选择期望测试服
		self.select_game_server()
		# 点击 开始
		self.loginPage.click_start()
		# 等待 登录成功
		self.newpoco('btnHome2').wait_for_appearance()
		# 如果出现收益弹窗，则关闭弹窗
		Logicoperation(self.newpoco).assert_offline_benefits_and_click_confirm()
		# 如果出现特权周卡弹窗，则关闭弹窗
		Logicoperation(self.newpoco).assert_weekly_card_pop_view_and_click_empty()
		time.sleep(1)

	def create_and_login_game(self, account):
		"""创建游戏账号并登录"""
		# 首次打开app,如果有弹窗，则关闭
		if self.newpoco('btnClose').exists():
			BaseOperation(self.newpoco).click_close()
			time.sleep(0.5)
		# 输入账号
		self.input_account_text(account)
		# 选择区服
		self.select_game_server()
		# 点击 开始
		self.loginPage.click_start()
		# 选择默认形象
		time.sleep(3)
		self.newpoco('btnConfirm').wait_for_appearance()
		self.base.click_confirm()
		# 选择第一个形象
		time.sleep(3)
		self.base.click_select()
		# 断言 进入 凡人修仙 页（有 btnJump元素出现）
		time.sleep(3)
		self.bassert.assert_exist_btnJump()
		# 点击 进入汴梁
		self.base.click_jump()
		# 点击 确定
		self.base.click_confirm()
		# 点击 空白处， 进入游戏
		self.base.click_empty()

