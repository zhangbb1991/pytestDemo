# -*- coding:utf-8 -*-

import logging.handlers
import datetime
import os
import inspect
import glob
import socket


class ReportLog(object):
    def __init__(self):
        pass

    def logdir(self):
        """日志路径"""
        current_path = os.path.abspath(__file__)
        parent_path = os.path.dirname(current_path)
        pparent__path = os.path.dirname(parent_path)
        log_dir = os.path.join(pparent__path, 'log')

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        return log_dir

    def __html_report_name(self, file):
        """
        :return: simple_report的html报告名称: 脚本名称 + 时间
        """
        path = os.path.abspath(file)
        filename = os.path.basename(path)
        prefix, subfix = os.path.splitext(filename)
        now = datetime.datetime.now()
        date_format = now.strftime('%Y-%m-%d-%H-%M-%S')
        output = prefix + '-' + date_format + '.' + 'html'
        return output

    def __txt_report_name(self, file):
        """
        :return:simple_report的logfile报告名称: 脚本名称 + 时间
        """
        path = os.path.abspath(file)
        filename = os.path.basename(path)
        prefix, subfix = os.path.splitext(filename)
        now = datetime.datetime.now()
        date_format = now.strftime('%Y-%m-%d-%H-%M-%S')
        output = 'log.txt'
        return output

    def html_report_output(self, file=__file__):
        """
        :return:  simple_report的html报告名称(output的值，包含路径): 路径 + 文件名称
        """
        log_dir = self.logdir()
        html_name = self.__html_report_name(file)
        return os.path.join(log_dir, html_name)

    def txt_logfile(self, file=__file__):
        """
        :return:  simple_report的logfile名称(logfile的值，包含路径): 路径 + 文件名称
        """
        log_dir = self.logdir()
        txt_name = self.__txt_report_name(file)
        full_path = os.path.join(log_dir, txt_name)
        return full_path

    def get_current_class_and_function_name(self, frame=None):
        """
        :return: 获取当前类和函数的名称
        """
        if not frame:
            frame = inspect.currentframe()
        class_name = frame.f_back.f_locals.get('self', None).__class__.__name__
        function_name = frame.f_back.f_code.co_name
        return class_name, function_name

    def join_class_function_name(self, frame=None):
        """
        :return: 拼接 类名和函数名， class-function
        """
        if not frame:
            frame = inspect.currentframe()
        class_name, function_name = self.get_current_class_and_function_name(frame)
        if class_name != 'NoneType' and function_name != 'NoneType':
            ret = class_name + '-' + function_name
        elif class_name == 'NoneType' and function_name != 'NoneType':
            ret = function_name
        elif class_name != 'NoneType' and function_name == 'NoneType':
            ret = class_name
        return ret

    def name_txt_and_html(self, frame=None):
        """
        :return: txt和html文件名称，不含路径
        """
        if not frame:
            frame = inspect.currentframe()
        prefix = self.join_class_function_name(frame)
        # 获取当前日期字符串
        date_str = datetime.datetime.now().strftime('%Y%m%d')

        # 获取递增数字，基于已存在的文件
        next_num = self._get_next_file_number(prefix, date_str)
        # 构造文件名
        txt_file = f"{prefix}-{date_str}-{next_num}.txt"
        html_file = f"{prefix}-{date_str}-{next_num}.html"
        return txt_file, html_file

    def full_txt_and_html(self, frame=None):
        """
        :return: txt和html全路径文件名称
        """
        if not frame:
            frame = inspect.currentframe()
        txt_file, html_file = self.name_txt_and_html(frame)
        log_dir = self.logdir()
        full_txt_file = os.path.join(log_dir, txt_file)
        full_html_file = os.path.join(log_dir, html_file)
        return full_txt_file, full_html_file

    def rt_dir_txt_html(self, test_case_name=None, frame=None):
        """
        :return:返回logdir,txt全路径文件名称，html全路径文件名称
        """
        log_dir = self.logdir()
        if test_case_name is None:
            # 如果没有提供测试用例名称，则使用调用该方法的函数名称
            frame = frame or  inspect.currentframe().f_back
            test_case_name = self.join_class_function_name(frame)

        # 获取递增数字，基于已存在的文件
        date_str = datetime.datetime.now().strftime('%Y%m%d')
        next_num = self._get_next_file_number(test_case_name, date_str)

        # 构造 txt和html文件名
        txt_file = f"{test_case_name}-{date_str}-{next_num}.txt"
        html_file = f"{test_case_name}-{date_str}-{next_num}.html"

        # 拼接全路径文件名
        full_txt_file = os.path.join(log_dir, txt_file)
        full_html_file = os.path.join(log_dir, html_file)
        return log_dir, full_txt_file, full_html_file


    def _get_next_file_number(self, prefix, date_str):
        max_num = -1
        # 构建两种文件的模式
        log_dir = self.logdir()
        txt_pattern = os.path.join(log_dir, f"{prefix}-{date_str}-*.txt")
        html_pattern = os.path.join(log_dir, f"{prefix}-{date_str}-*.html")
        # 进行 glob 搜索
        existing_files_txt = glob.glob(txt_pattern)
        existing_files_html = glob.glob(html_pattern)
        existing_files = existing_files_txt + existing_files_html
        # 查找现有文件中的最大序号
        for filepath in existing_files:
            filename = os.path.basename(filepath)
            try:
                num = int(filename.split('-')[-1].split('.')[0])
                max_num = max(max_num, num)
            except ValueError:
                pass
        return max_num + 1

    def get_local_ip(self):
        try:
            # 创建一个 socket 对象
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 不需要真正连接到服务器，所以目标可以是任意服务器和端口
            s.connect(("8.8.8.8", 80))
            # 获取本地 IP 地址
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            print("无法获取本地 IP，原因：", e)
            return None


class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        'DEBUG': '\033[94m',  # 蓝色
        'INFO': '\033[92m',  # 绿色
        'WARNING': '\033[93m',  # 黄色
        'ERROR': '\033[91m',  # 红色
        'CRITICAL': '\033[91m'  # 红色
    }
    RESET_CODE = '\033[0m'

    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        color_code = self.COLOR_CODES.get(levelname, '')
        reset_code = self.RESET_CODE if color_code else ''
        formatted_message = f'{color_code}{message}{reset_code}'
        return formatted_message


class ColoredFileHandler(logging.FileHandler):
    def __init__(self, log_dir=None, mode='a', encoding=None, delay=False):
        today = datetime.date.today()
        filename = f'{log_dir}/{today.strftime("%Y-%m-%d")}.log'
        super().__init__(filename, mode, encoding, delay)


log_dir = ReportLog().logdir()


def logger(log_dir=log_dir, level='INFO'):
    log = logging.getLogger()
    log.handlers.clear()

    level = getattr(logging, level)
    log.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = ColoredFormatter('%(asctime)s  %(levelname)s %(lineno)d --- [%(filename)s] : %(message)s')
    console_handler.setFormatter(console_formatter)
    log.addHandler(console_handler)
    file_handler = ColoredFileHandler(log_dir)
    file_handler.setLevel(level)
    file_formatter = logging.Formatter('%(asctime)s  %(levelname)s %(lineno)d --- [%(filename)s] : %(message)s')
    file_handler.setFormatter(file_formatter)
    log.addHandler(file_handler)
    return log


__all__ = ['logger']

if __name__ == '__main__':
    logger = logger()
#     logger.debug('This is a debug message')
#     logger.info('This is an info message')
#     logger.warning('This is a warning message')
#     logger.error('This is an error message')
#     logger.critical('This is a critical message')

# rp = ReportLog()
# ip = rp.get_local_ip()
# print(ip)
# txt,html = rp.name_txt_and_html()
# print(txt, html)

#     html_file = rp.html_report_output()
#     txt_file = rp.txt_logfile()
#     print(html_file)
#     print(txt_file)
# obj = MyClass()
# obj.my_method()
