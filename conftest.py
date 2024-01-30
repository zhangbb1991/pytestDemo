import time
import pytest
from hytest import GSTORE
from poco.drivers.cocosjs import CocosJsPoco
from utils.myAirtest import myAirTest
from airtest.core.api import auto_setup
from utils.mylog import ReportLog
from launch import App

mylogger = ReportLog()
myair = myAirTest()

"""
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
"""


# 启动APP
@pytest.fixture(scope='module', autouse=True)
def connect_phone():
    devices = myAirTest().readIniDevices('common', 'devices')[0]
    package = myAirTest().readIniConf('common', 'package')
    platform, uuid = devices.split("://")[0], devices.split("://")[1].split("?")[0]
    App(platform, uuid, package).start()
    time.sleep(15)
    devices = myAirTest().readIniDevices('common', 'devices')
    auto_setup(__file__, logdir=True, devices=devices)


# poco初始化，返回poco对象
@pytest.fixture(scope='module', autouse=True)
def newpoco(connect_phone):
    newpoco = CocosJsPoco()
    GSTORE['newpoco'] = newpoco
    return newpoco



# 报告生成
@pytest.fixture(scope='function', autouse=True)
def generate_report(request):
    devices = myAirTest().readIniDevices('common', 'devices')
    log_dir, test_log_file, output_file = mylogger.rt_dir_txt_html(test_case_name=request.node.name)
    myair.custom_auto_setup(__file__, logdir=log_dir, logfile=test_log_file, devices=devices)
    yield
    myair.custom_report(file=__file__, log_dir=log_dir, test_log_file=test_log_file, output_file=output_file)


# 每个测试脚本执行完，退出app
@pytest.fixture(scope='module', autouse=True)
def teardown_per_module(newpoco):
    yield
    devices = myAirTest().readIniDevices('common', 'devices')[0]
    package = myAirTest().readIniConf('common', 'package')
    platform, uuid = devices.split("://")[0], devices.split("://")[1].split("?")[0]
    App(platform, uuid, package).quit()
