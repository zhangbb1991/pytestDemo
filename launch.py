# -*- coding:utf-8 -*-

import re
import shutil
import sys
import time

import requests
from airtest.core.api import *
from utils.myAirtest import myAirTest
from bs4 import BeautifulSoup
import subprocess


class DownLoadApk():
	def __init__(self, build_url):
		self.jenkins_console_url = build_url + 'console' # 传入 build_url组装jenkins_console_url，build_url如http://d-jenkins.xmyanqu.cn/job/Client-tw-6.0/8489/
		self.jenkins_headers = {
			'Authorization': 'Basic emhhbmdiaW5nYmluZzoxMTM1NjU2ZGJiMTZlZDUyM2U3ZjMxNzEyMDFlYTA0YzQ3'
		}

	def get_download_link(self):
		"""获取安装包的下载链接"""
		# 发送请求获取控制台输出
		response = requests.get(self.jenkins_console_url, headers=self.jenkins_headers)
		if response.status_code == 200:
			# 解析html内容
			soup = BeautifulSoup(response.text, 'html.parser')
			# 定义正则表达式
			pattern = r'.*.APK下载地址:.*'
			# 查找所有的匹配
			matches = re.findall(pattern, str(soup))
			if matches:
				ret = matches[0]
				pattern2 = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+(?:[\w./-]+)+\.apk"
				matches2 = re.search(pattern2, ret)
				if matches2:
					download_link = matches2.group()
					return download_link
			else:
				print('未找到匹配的下载链接')
		else:
			print(f"请求失败，状态码: {response.status_code}")

	def download_apk(self):
		"""下载安装包"""
		download_link = self.get_download_link()
		file_name = 'auto-test-jwdzg.apk'
		print(time.asctime())
		response = requests.get(download_link)

		with open(file_name, 'wb') as f:
			f.write(response.content)
		print(f"安装包已下载到 {file_name}")
		print(time.asctime())
		return file_name

	def push_apk_to_device(self, apk_name, device_id):
		"""推送apk安装包到测试机上"""
		tmp_path = "/data/local/tmp/"
		# 检查 adb是否可用
		if not shutil.which('adb'):
			raise ValueError('ADB not found in PATH')

		# 设置目标设备
		if device_id:
			subprocess.run(["adb", "devices"], check=True)  # 列出所有设备及状态
			subprocess.run(["adb", "-s", device_id, "wait-for-device"], check=True)  # 等待指定设备ID的设备变为可用

		# 检查设备上是否存在同名文件
		output = subprocess.check_output(["adb", "-s", device_id, "shell", "ls", f"{tmp_path}"])
		print(output)
		existing_files = output.decode().split()
		print(existing_files)
		if os.path.basename(apk_name) in existing_files:
			print(os.path.basename(apk_name))
			# 删除设备上的同名文件
			subprocess.run(["adb", "-s", device_id, "shell", "rm", f"{tmp_path}{os.path.basename(apk_name)}"], check=True)
		# 将apk文件推送到设备
		subprocess.run(["adb", "-s", device_id, "push", apk_name, f"{tmp_path}"], check=True)
		# 增加一个校验步骤，判断是否推送成功
		output = subprocess.check_output(["adb", "-s", device_id, "shell", "ls", f"{tmp_path}"])
		if os.path.basename(apk_name) not in output.decode().split():
			raise Exception("APK23文件未成功推送到设备上")

	def stop(self, package):
		"""停止应用
			package：包名，如game.yanqu.TheSilkRoad.tw
		"""
		subprocess.run(["adb", "-s", device_id, "shell", "am", "force-stop", package], check=True)

	def uninstall(self, package, device_id):
		"""卸载旧包
			package：包名，如game.yanqu.TheSilkRoad.tw
		"""
		# 检查设备上是否已安装同名应用
		output = subprocess.check_output(["adb", "-s", device_id, "shell", "pm", "list", "packages"])
		installed_packages = output.decode().splitlines()

		package_tring = 'package:' + package  # 组装成'package:game.yanqu.TheSilkRoad.tw' 到installed_packages里去校验
		if package_tring in installed_packages:
			# 先停止应用
			self.stop(package)
			# 卸载旧版应用
			subprocess.run(["adb", "-s", device_id, "uninstall", package], check=True)
			print('卸载命令执行完成')
			# 检查应用是否已经被卸载
			output_after_uninstall = subprocess.check_output(["adb", "-s", device_id, "shell", "pm", "list", "packages"])
			installed_packages_after_uninstall = output_after_uninstall.decode().splitlines()
			if package_tring in installed_packages_after_uninstall:
				raise Exception("旧包未卸载成功")
			else:
				print("旧包卸载成功")

	def install(self, apk_name, device_id, package):
		"""安装新包"""
		tmp_path = "/data/local/tmp/"
		subprocess.run(["adb", "-s", device_id, "shell", "pm", "install", "-r", f"{tmp_path}{os.path.basename(apk_name)}"], check=True)
		package_string = 'package:' + package
		# 检查是否安装成功
		output_after_install = subprocess.check_output(["adb", "-s", device_id, "shell", "pm", "list", "packages"])
		installed_packages_after_install = output_after_install.decode().splitlines()
		if package_string in installed_packages_after_install:
			print("新包安装成功")
		else:
			raise Exception("新包安装失败")

class App():
	def __init__(self, platform, uuid, package):
		print('尝试连接设备')
		connect_device(f"{platform}://{uuid}")
		dev = device()
		print('设备连接成功')
		self.myAir = myAirTest()
		self.package = package

	def start(self):
		time.sleep(5)
		print('尝试启动APP')
		start_app(self.package)
		print('启动APP成功')

	def quit(self):
		print('准备关闭app')
		stop_app(self.package)
		time.sleep(5) # 等待连接释放
		print('关闭APP成功')


if __name__ == '__main__':
	devices = myAirTest().readIniDevices('common', 'devices')[0]
	package = myAirTest().readIniConf('common', 'package')
	device_id = myAirTest().readIniConf('common', 'device_id')
	platform, uuid = devices.split("://")[0], devices.split("://")[1].split("?")[0]

	# 装包
	if len(sys.argv) < 2:
		print("Usage: python launch.py <build_url>")
		sys.exit(1)
	build_url = sys.argv[1]
	downLoadApk = DownLoadApk(build_url)
	download_link = downLoadApk.get_download_link()
	print(download_link)
	apk = downLoadApk.download_apk()
	downLoadApk.push_apk_to_device(apk, device_id)
	downLoadApk.uninstall(package, device_id)
	downLoadApk.install(apk, device_id, package)
	# 启动App
	app = App(platform, uuid, package)
	app.start()
	# time.sleep(5)
	# app.quit()
