#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-15 14:26:19
# @Author  : robin (robin.zhu@nokia.com)
# @Description : 文件内容重新排列

import os,shutil,time
desktop_path = 'D:\\userdata\\myselfname\Desktop'

def sort_file(file_name):
	file = open(file_name,"r")
	contents = file.readlines()
	contents.sort()
	file.close()
	file = open(file_name,"w+")
	file.writelines(contents)
	file.close()

def begain_sort(root_path):
	count=60
	while(count):
		for root,dirs,files in os.walk(root_path):
			if files:
				for file in files:
					file_name = os.path.join(root,file)	
					sort_file(file_name)
					new_file_name = os.path.join(desktop_path,file)
					shutil.move(file_name,new_file_name)
			else:
				time.sleep(2)
				count = count - 2
				print 'count:',count 

if __name__ == '__main__':
	#sort_file('ecl_dsp.txt')
	src_path = 'D:\\userdata\\myselfname\Desktop\\file_sort_factory'
	begain_sort(src_path)
	





