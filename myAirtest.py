#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import allure
import configparser
from airtest.core.api import *
from airtest.core.settings import Settings as ST
from airtest.report.report import simple_report
from mylog import ReportLog

class myAirTest(object):


	def __init__(self):
		self.mylogger = ReportLog()

	def custom_auto_setup(self,basedir=None, devices=None, logdir=None, project_root=None, compress=None, logfile=None):
		"""
		:return:
		"""
		open(logfile, 'w').close()
		ST.LOG_FILE = logfile

		if basedir:
			if os.path.isfile(basedir):
				basedir = os.path.dirname(basedir)
			if basedir not in G.BASEDIR:
				G.BASEDIR.append(basedir)
		if devices:
			print('do nothing')

		if logdir:
			logdir = script_log_dir(basedir, logdir)
			set_logdir(logdir)
		if project_root:
			ST.PROJECT_ROOT = project_root
		if compress:
			ST.SNAPSHOT_QUALITY = compress

	def custom_report(self, file, log_dir, test_log_file, output_file):
		simple_report(file, logpath=log_dir, logfile=test_log_file, output=output_file)
		ip = self.mylogger.get_local_ip()
		absolute_output_file_path = os.path.abspath(output_file)
		report_url = f"http://{ip}:8000/{absolute_output_file_path}"
		allure.dynamic.link(report_url, name='查看Airtest报告')

	def readIniConf(self, section, option):
		"""
		读取pytest.ini配置文件的内容
		"""
		current_path = os.path.abspath(__file__)
		parent_path = os.path.dirname(current_path)
		#ini_file = os.path.join(os.path.dirname(parent_path), 'pytest.ini')
		ini_file = os.path.join(parent_path, 'pytest.ini')
		print(ini_file)
		conf = configparser.ConfigParser()
		conf.read(ini_file, encoding='utf-8')
		# 获取配置项
		ret = conf.get(str(section), str(option))
		return ret

	def readIniDevices(self, section, option):
		"""
		读取pytest.ini配置的devices,返回列表
		"""
		ret_str = self.readIniConf(section, option)
		ret_list = ret_str.strip('][').split(', ')
		return ret_list



if __name__ == '__main__':
	myAir = myAirTest()
	ret = myAir.readIniDevices('common', 'devices')
	print(ret)







