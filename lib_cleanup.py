#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-21 10:29:36
# @Author  : robin (robin.zhu@nokia.com)


import os,time,sys
from os import path as PT

def delete_libs_by_time(dir_name,keep_days=30):
	try:
		now_time = time.time()
		keep_seconds = keep_days*24*60*60
		for root,dirs,files in os.walk(dir_name):
			for file in [zipfile for zipfile in files if "zip" in zipfile]:
				file_full_name = PT.join(root,file)
				last_time = PT.getmtime(file_full_name)
				if (now_time - last_time) > keep_seconds:
					os.remove(file_full_name)
					print "removing {0},file date{1}：".format(file_full_name,time.ctime(last_time))
	except Exception as e:
		print  e

if __name__ == '__main__':
	dir_name = sys.argv[1]
	delete_libs_by_time(dir_name)

         

