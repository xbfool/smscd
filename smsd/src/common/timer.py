#!/usr/bin/env python
# coding=utf-8
"""
@file timer.py
@author hitzheng@tencent.com
@version 1.0
@date 2011-9-21
@brief ��ʱ����صķ�װ����Ҫ����ʱ����صĲ���
"""

import time

class Timer:
	def __init__(self):
		self.tmBegin = time.time()
	
	def elapse(self):
		"""���˶��ٺ���"""
		tmEnd = time.time()
		return int((tmEnd - self.tmBegin)*10**3)
		
	def elapseUs(self):
		"""���˶���΢��"""
		tmEnd = time.time()
		return int((tmEnd - self.tmBegin)*10**6)
		
	def elapseS(self):
		"""���˶�����"""
		tmEnd = time.time()
		return int(tmEnd - self.tmBegin)

if __name__ == "__main__":
	tm = Timer()
	time.sleep(2)
	print "time elaps %d s" % tm.elapseS()
	print "time elaps %d ms" % tm.elapse()
	print "time elaps %d us" % tm.elapseUs()
	
