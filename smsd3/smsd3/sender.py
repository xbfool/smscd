#!/usr/bin/env python
# -*- coding: utf-8 -*-

import channels.honglian.sender as sender
from channels.setting.settings import settings

def run():
    try:
        print sender.send('honglian_tyb', '18616820727', 'test ctyb！', settings)
        #print sender.send('honglian_bjyh', '18616820727', '您好！文件（出库单/药检）已于5月22日寄出，速尔单号：821354869462，请注意查收！浙江灵康。', settings)
        #print sender.send('honglian_jtyh', '18616820727', '您好！文件（出库单/药检）已于5月22日寄出，速尔单号：821354869462，请注意查收！浙江灵康。', settings)
        #print sender.send('honglian_tyb', '18616820727', '您好！文件（出库单/药检）已于5月22日寄出，速尔单号：821354869462，请注意查收！浙江灵康。', settings)
        #print sender.send('honglian_tyd', '18616820727', '您好！文件（出库单/药检）已于5月22日寄出，速尔单号：821354869462，请注意查收！浙江灵康。', settings)
        #print sender.send('honglian_mock', '18616820727', '您好！文件（出库单/药检）已于5月22日寄出，速尔单号：821354869462，请注意查收！浙江灵康。', settings)
    except:
        pass
    
from timeit import Timer
t = Timer("run()", "from __main__ import run")
print t.timeit(1)
