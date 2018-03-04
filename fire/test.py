#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-16 11:56:17
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    : 

import os,fire

class A1(object):
	"""docstring for A1"""
	def __init__(self, arg):
		self.arg = arg

	def fun1(self):
		print self.arg

	def fun2(self,name):
		print name

	@classmethod
	def fun3(cls,age):
		print age

	@staticmethod
	def fun4(sex):
		print sex

def a1(name,age,sex):
	print name
	print age
	print sex


if __name__ == '__main__':
	fire.Fire(a1)
	# fire.Fire(A1)