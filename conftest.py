import time
import pytest
from hytest import GSTORE
from poco.drivers.cocosjs import CocosJsPoco
from myAirtest import myAirTest
from airtest.core.api import auto_setup
from mylog import ReportLog
from launch import App

mylogger = ReportLog()
myair = myAirTest()


# 本地调试单个脚本使用

@pytest.fixture(scope='session', autouse=True)
def connect_phone():
    devices = myAirTest().readIniDevices('common', 'devices')
    auto_setup(__file__, logdir=True, devices=devices)

@pytest.fixture(scope='session', autouse=True)
def newpoco(connect_phone):
    newpoco = CocosJsPoco()
    GSTORE['newpoco'] = newpoco
    return newpoco
