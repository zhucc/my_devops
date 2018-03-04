#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-11 13:01:54
# @Author  : robin (robin.zhu@nokia.com)
# @Link    : http://example.org
# @Version : $Id$

import os,sys
from os import path as PT
def change_soft_link(root_path):
	for root,dirs,files in os.walk(root_path):
		for file in files:
			full_name = PT.join(root,file)
			if PT.islink(full_name):
				link_content = os.readlink(full_name)
				print "{0} -> {1}".format(full_name,link_content)
		for dir in dirs:
			full_name = PT.join(root,dir)
			if PT.islink(full_name):
				link_content = os.readlink(full_name)
				print "{0} -> {1}".format(full_name,link_content)
					
if __name__ == '__main__':
	root_path = sys.argv[1]
	change_soft_link(root_path)
