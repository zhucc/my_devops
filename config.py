#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-17 23:11:29
# @Author  : robin (robin.zhu@nokia.com)
# @Description : 

import ConfigParser

jenkins_config_info = {}
def get_all_config():
	try:
		config = ConfigParser.ConfigParser()
		config.read('configfile.conf')
		for section in config.sections():
			for option in config.options(section):
				jenkins_config_info[option] = config.get(section,option)
	except Exception as e:
		print e


if __name__ == '__main__':
	get_all_config()
	for key,value in jenkins_config_info.items():
		print key,">>",value
