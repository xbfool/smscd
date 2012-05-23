#!/usr/bin/env python
# coding=utf-8
"""
@file timer.py
@author hitzheng@tencent.com
@version 1.0
@date 2011-9-21
@brief 定时器相关的封装，主要处理时间相关的操作
"""

import time

class Timer:
	def __init__(self):
		self.tmBegin = time.time()
	
	def elapse(self):
		"""过了多少毫秒"""
		tmEnd = time.time()
		return int((tmEnd - self.tmBegin)*10**3)
		
	def elapseUs(self):
		"""过了多少微秒"""
		tmEnd = time.time()
		return int((tmEnd - self.tmBegin)*10**6)
		
	def elapseS(self):
		"""过了多少秒"""
		tmEnd = time.time()
		return int(tmEnd - self.tmBegin)

if __name__ == "__main__":
	tm = Timer()
	time.sleep(2)
	print "time elaps %d s" % tm.elapseS()
	print "time elaps %d ms" % tm.elapse()
	print "time elaps %d us" % tm.elapseUs()
	
