# -*- coding:utf-8 -*-
from airtest.core.api import *
from mylog import logger
from myAirtest import myAirTest


class BaseOperation(object):
	def __init__(self, newpoco):
		self.newpoco = newpoco
		self.log = logger()

	def templete(self, image):
		curdir = os.path.dirname(os.path.abspath(__file__))
		template_path = os.path.join(curdir, 'images', image)
		touch(Template(template_path))

	def __click_button(self, locator):
		self.log.info(f'点击控件： {locator}')
		self.newpoco(locator).wait_for_appearance()
		return self.newpoco(locator).click()

	def click_button2(self,locator1, locator2):
		self.log.info(f'点击控件：{locator1} > {locator2}')
		self.newpoco(locator1).offspring(locator2).wait_for_appearance()
		self.newpoco(locator1).offspring(locator2).click()

	def click_button3(self, locator1, locator2, locator3):
		self.log.info(f'点击控件：{locator1} > {locator2} > {locator3}')
		self.newpoco(locator1).offspring(locator2).offspring(locator3).wait_for_appearance()
		self.newpoco(locator1).offspring(locator2).offspring(locator3).click()


	def click_finger(self):
		"""点击引导层的手指"""
		self.__click_button('imgMask')


	# 点击 关闭
	def click_close(self):
		self.log.info('点击 关闭')
		self.__click_button('btnClose')

	# 点击 跳转
	def click_jump(self):
		self.log.info('点击 跳转')
		self.__click_button('btnJump')

	# 点击 取消
	def click_cancel(self):
		self.log.info('点击 取消')
		self.__click_button('btnCancel')

	# 点击 确认
	def click_confirm(self):
		self.log.info('点击 确认')
		self.__click_button('btnConfirm')

	# 选择，默认选择第1个
	def click_select(self, idx=0):
		self.log.info('点击 选择')
		self.newpoco('ListItem').wait_for_appearance()
		self.newpoco('ListItem')[idx].offspring('btnSelect').click()

	# 点击 空白区域(暂时取 headLayer)
	def click_empty(self):
		self.log.info('点击 空白区域')
		self.__click_button('headLayer')
		time.sleep(0.5)
		#self.__click_button('Main') # 调试 手机兼容性
		#self.newpoco([0.6, 0.7]).click() # 调试 手机兼容性 [No]
		# self.__click_button('mainLayer') 调试手机兼容性 [No]
		#self.__click_button('taskItem')

	# 点击 提示
	def click_task_item(self):
		self.log.info('点击 任务提示')
		self.__click_button('taskItem')

	# 点击 打勾✔
	def click_check(self):
		self.log.info('点击 打勾✔(任务完成确认)')
		self.__click_button('n8')

	# 点击 点击继续(也可用 ‘txtDialog’)
	def click_lab_tips(self):
		self.log.info('点击 点击继续')
		self.__click_button('labTips')

	# 点击 前往(主线任务 frame 的 前往)
	def click_go(self):
		self.log.info('点击 前往')
		self.__click_button('btnGo')

	# 点击 建造
	def click_build(self):
		self.log.info('点击 建造')
		self.__click_button('btnBuild')

	# 主页 的建造
	def click_unlock(self):
		self.log.info('点击 主页上的 建造 提示')
		self.__click_button('unlockItem')

	# 点击 招募
	def click_get(self):
		self.log.info('点击 招募')
		self.__click_button('btnGet')

	# 点击 升级
	def click_upgrade(self):
		self.log.info('点击 提升')
		self.__click_button('btnUpgrade')

	# 点击 升级
	def click_up(self):
		self.log.info('点击 提升')
		self.__click_button('btnUp')

	def click_two_skill_upgrade(self):
		self.log.info('点击 升级(技能升级)')
		#self.__click_button('btnTwoSkillUpgrade')
		#self.newpoco('btnTwoSkillUpgrade').offspring("btnCover").click()
		self.templete('two_skill_upgrade.png')


	# 点击 钱庄
	def click_bank(self):
		self.log.info('点击 钱庄')
		#self.__click_button('bankInfoItem') 会偶尔误差
		self.newpoco('bankInfoItem').offspring('txtName').wait_for_appearance()
		self.newpoco('bankInfoItem').offspring('txtName').click()

	# 点击 医馆
	def click_infirmary(self):
		self.log.info('点击 医馆')
		#self.newpoco('infoItem105000').offspring("realInfoItem").offspring("txtName").click() # 调试可用
		curdir = os.path.dirname(os.path.abspath(__file__))
		template_path = os.path.join(curdir, 'images', 'infirmary_icon.png')
		touch(Template(template_path))

	# 点击 effectLayer 的 手指
	def click_effect_finger(self):
		self.log.info('点击 手指')
		self.newpoco('effectLayer').offspring('NoviceGuide').offspring('fingerItem').wait_for_appearance()
		self.newpoco('effectLayer').offspring('NoviceGuide').offspring('fingerItem').click()

	# 点击 钱庄扩建
	def click_bank_expand(self):
		self.log.info('点击 钱庄扩建')
		self.__click_button('bankExpandItem')

	# 点击 扩建 按钮
	def click_expand(self):
		self.log.info('点击 扩建 按钮')
		self.__click_button('btnExpand')

	# 点击 九龙城寨
	def click_kow_loon(self):
		self.log.info('点击 九龙城寨')
		self.__click_button('kowLoonInfoItem')

	# 点击 身份头像
	def click_head_icon(self):
		self.log.info('点击 身份头像')
		self.__click_button('headIconItem')

	# 点击 贸易
	def click_trade(self):
		self.log.info('点击 贸易')
		self.__click_button('btnTrade')

	# 点击 议价
	def click_attack(self):
		self.log.info('点击 议价')
		self.__click_button('btnAttack')

	def click_attack_idx(self, idx):
		"""点击 第idx个 InfoItem 下的 btnAttack """
		self.log.info(f'点击 第{idx}个 InfoItem 下的 btnAttack')
		self.newpoco('InfoItem')[idx].offspring('btnAttack').click()

	def click_new_build(self):
		self.log.info('点击 建造 提示')
		curdir = os.path.dirname(os.path.abspath(__file__))
		template_path = os.path.join(curdir,'images', 'build_icon.png')
		touch(Template(template_path))

	def click_drugstore(self):
		self.log.info('点击 药铺')
		curdir = os.path.dirname(os.path.abspath(__file__))
		template_path = os.path.join(curdir, 'images', 'drugstore_icon.png')
		touch(Template(template_path))

	def click_storeteller(self):
		self.log.info('点击 说书摊')
		curdir = os.path.dirname(os.path.abspath(__file__))
		template_path = os.path.join(curdir, 'images', 'storyteller_icon.png')
		touch(Template(template_path))

	def click_deployment(self):
		self.log.info('点击 门客委任 提示符号')
		curdir = os.path.dirname(os.path.abspath(__file__))
		template_path = os.path.join(curdir, 'images', 'deployment_icon.png')
		touch(Template(template_path))

	def deploy_zgn(self):
		self.log.info('委任门客 郑果农')
		self.templete('deploy_zgn.png')

	def click_recycle(self):
		"""点击 放归"""
		self.__click_button('btnRecycle')

	def clear_input_text(self, locator):
		"""清空输入框文本"""
		current_text = self.newpoco(locator).get_text()
		for char in current_text:
			keyevent('KEYCODE_DEL')

	def swipe(self, locator1, locator2):
		"""根据loctator2的position计算出locator1的滑动方向并滑动"""
		pos = self.newpoco(locator2).get_position()
		pos_target = [-(pos[0]-0.5), -(pos[1]-0.5)]
		if (pos[0] > 1 and pos[1] > 0 and pos[1] < 1):
			pos_target = [-(pos[0] - 0.99), 0]
			self.newpoco(locator1).swipe(pos_target)
		elif (pos[1] > 1 and pos[0] > 0 and pos[0] < 1):
			pos_target = [0, -(pos[1] - 1)]
			self.newpoco(locator1).swipe(pos_target)
		elif (pos[0] < 0 and pos[1] > 0 and pos[1] < 1):
			pos_target = [-(pos[0] - 0.1), pos[1]]
			self.newpoco(locator1).swipe(pos_target)
		time.sleep(1)


class BaseGetNodeInfo(object):
	"""获取元素的文本信息"""

	def __init__(self, newpoco):
		self.newpoco = newpoco
		self.log = logger()

	def get_task_txt_condition(self):
		"""
		:return: 获取主线任务的条件，用于计算需要操作的次数
		"""
		ret = self.newpoco('taskItem').offspring('taskTxtCondition').get_text()
		return ret

	def get_task_txt_name(self):
		"""
		:return: 获取主线任务的文本
		"""
		ret = self.newpoco('taskItem').offspring('taskTxtName').get_text()
		return ret

	def get_text(self, locator):
		"""获取元素的文本"""
		self.newpoco(locator).wait_for_appearance()
		ret = self.newpoco(locator).get_text()
		return ret

	def get_text_int(self, locator):
		"""获取元素的文本, 返回int型"""
		self.newpoco(locator).wait_for_appearance()
		ret = self.newpoco(locator).get_text()
		return int(ret)


class BaseOperationHome(object):
	"""home栏封装"""

	# def __init__(self):
	# 	self.newpoco = CocosJsPoco()
	# 	self.log = logger()

	def __init__(self, newpoco):
		self.newpoco = newpoco
		self.log = logger()

	# 点击 Home栏
	def __click_btn_home(self, idx):
		locator = 'btnHome' + str(idx)
		self.newpoco(locator).click()

	# idx=1:府邸 idx=2 商铺 idx=3:门客 idx=4:关卡 idx=5:城郊 idx=6:背包
	# 点击 府邸
	def click_mansion(self):
		self.log.info('点击 府邸')
		self.__click_btn_home(1)

	# 点击 商铺
	def click_market(self):
		self.log.info('点击 商铺')
		self.__click_btn_home(2)

	# 点击 门客
	def click_retainer(self):
		self.log.info('点击 门客')
		self.__click_btn_home(3)

	# 点击 关卡
	def click_stage(self):
		self.log.info('点击 关卡')
		self.__click_btn_home(4)

	# 点击 城郊
	def click_suburb(self):
		self.log.info('点击 城郊')
		self.__click_btn_home(5)

	# 点击 背包
	def click_bag(self):
		self.log.info('点击 背包')
		self.__click_btn_home(6)

class OperateApp(object):
	"""游戏APP操作"""
	def __init__(self, newpoco):
		super().__init__(newpoco)
		self.myAir = myAirTest()
		self.package = self.myAir.readIniConf('common', 'package')
		self.width, self.height = device().get_current_resolution()

	def is_app_running(self):
		"""检查应用是否在运行"""
		result = result = shell('ps | grep %s' % self.package)
		return self.package in result

	def start_app(self):
		# 先尝试关闭应用，确保从干净的状态开始
		if self.is_app_running():
			self.stop_app()
		# 启动应用
		start_app(self.package)
		# 检查应用是否启动成功
		max_wait_time = 10
		waited_time = 0
		while waited_time < max_wait_time:
			if self.is_app_running():
				time.sleep(20)  # 等待页加载
				print('App启动成功')
				break
			else:
				time.sleep(1)
				waited_time += 1
		if waited_time == max_wait_time:
			print(f'{max_wait_time} 秒内，App未启动成功')

	def stop_app(self):
		stop_app(self.package)

	def clear_app(self):
		clear_app(self.package)

class PublicPromptPopup:
	"""提示弹窗 封装"""

	def __init__(self, newpoco, locator):
		self.locator = locator
		self.newpoco = newpoco
		self.log = logger()

	def click_button(self, locator):
		BaseOperation(self.newpoco).click_button2(self.locator, locator)

	def exist_locator(self, locator):
		self.newpoco(locator).exists()

	def assert_exist_prompt_popup(self):
		self.log.info('断言出现 弹窗')
		#self.newpoco(self.locator).exists()
		self.exist_locator(self.locator)

	def click_close(self):
		self.log.info('点击 关闭')
		self.click_button('btnClose')

	def click_cancel(self):
		self.log.info('点击 Cancel')
		self.click_button('btnCancel')

	def click_confirm(self):
		self.log.info('点击 Confirm')
		self.click_button('btnConfirm')

	def click_go(self):
		self.log.info('点击 Go')
		self.click_button('btnGo')

