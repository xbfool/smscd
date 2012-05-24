# coding=utf-8
"""
@file log.py
@author sunman.yang@gmail.com
@version 2.0
@date 2012-5-22
@brief 调用logging模块，产生按大小或天回滚的日志
@history:
"""

import logging
import logging.handlers
import os
import sys

#自定义级别，与logging对应
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR 
CRITICAL = logging.CRITICAL

def initLogger(loggername, dirname=".", level=DEBUG, backcnt=90):
	"""
	@brief 初始化日志，按天回滚，警告信息以上的单独放到一个按文件大小回滚的文件里
	@param loggername 日志名称, 错误名称为loggername+"_error"
	@param dirname 日志存放目录
	@param level 日志级别
	@param backcnt 存放备份个数
	@return 生成的日志对象
	"""
	
	#目录不存在，创建目录
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		
	#记录信息按天回滚
	trfFileName = os.path.join(dirname, loggername + ".log")
	trfHandler = logging.handlers.TimedRotatingFileHandler(trfFileName, 'midnight', backupCount = backcnt)
	trfHandler.setLevel(logging.DEBUG)
	
	#警告以上信息按文件大小(100M)回滚
	rfFileName = os.path.join(dirname, loggername + "_error.log")
	rfHandler = logging.handlers.RotatingFileHandler(rfFileName, maxBytes=102400000, backupCount=2)
	rfHandler.setLevel(logging.ERROR)
	
	#日志格式
	formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s')
	trfHandler.setFormatter(formatter)
	rfHandler.setFormatter(formatter)
	
	#logger对象
	logger = logging.getLogger(loggername)
	logger.setLevel(level)
	logger.addHandler(rfHandler)
	logger.addHandler(trfHandler)
	
	return logger

smsd_log_path = os.path.dirname(__file__) + "/../log/"
logger = initLogger("smsd", smsd_log_path)

if __name__ == "__main__":
	logger = initLogger("test")
	logger.debug("debug")
	logger.info("info")
	logger.warning("warning")
	logger.error("error")
	logger.critical("critical")
	
