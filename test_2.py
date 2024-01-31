#!/usr/bin/env python
# -*- coding:utf-8 -*-
""""""
import time

import airtest.core.device
import allure
from hytest import GSTORE
from mainPage import MainPage

from myAirtest import myAirTest
from mylog import ReportLog
from loginLogic import LoginLogic

myair = myAirTest()
mylogger = ReportLog()
air = airtest
account = 'gj00001'
devices = myair.readIniDevices('common', 'devices')


def setup_module():
    newpoco = GSTORE['newpoco']
    LoginLogic(newpoco).login_game(account)
    time.sleep(2)


def teardown_module():
    pass


def setup_function():
    newpoco = GSTORE['newpoco']


def teardown_function(newpoco):
    print()


def test_1(newpoco):
    with allure.step('点击 城郊'):
        MainPage(newpoco).click_suburb()
        time.sleep(1)
