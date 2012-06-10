# coding=utf-8
#!/usr/bin/env python


import time

class Timer:
	def __init__(self):
		self.tmBegin = time.time()
	
	def elapse(self):
		tmEnd = time.time()
		return int((tmEnd - self.tmBegin)*10**3)
		
	def elapseUs(self):
		tmEnd = time.time()
		return int((tmEnd - self.tmBegin)*10**6)
		
	def elapseS(self):
		tmEnd = time.time()
		return int(tmEnd - self.tmBegin)

if __name__ == "__main__":
	tm = Timer()
	time.sleep(2)
	print "time elaps %d s" % tm.elapseS()
	print "time elaps %d ms" % tm.elapse()
	print "time elaps %d us" % tm.elapseUs()
	
