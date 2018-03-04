#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-12 14:48:57
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    : 

import threading
# import asyncio,random,time
import wait


async def hello():
	print ("hello step 1")
	await wait()
	print ("hello step 2")


async def wait():
	aa = random.randint(3,10)
	print ("sleep {0} s".format(aa))
	lala = 1
	for i in range(1000000*aa):
		lala = i**3
	print ("wait end")

loop = asyncio.get_event_loop()
tasks = [ hello(),hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()