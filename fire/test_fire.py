#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-15 11:10:34
# @Author  : robin (robin.zhu@nokia.com)
# @Description : 

import os,fire

class huhu(object):
	"""docstring for huhu"""
	def __init__(self, arg):
		print arg,"."*20

	def fun_a(self):
		print "fun_a","."*20

	def fun_b(self):
		print "fun_b","."*20

def main():
	fire.Fire(huhu)

if __name__ == '__main__':
	main()