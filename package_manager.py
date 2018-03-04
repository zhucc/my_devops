#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-23 13:25:19
# @Author  : robin (robin.zhu@nokia.com)


import os,sys
from config import get_all_config
class LIB_MANAGER():
	"""
	manager lsp libs in some dir. exp:"/build/home/ca_hzpsscm/CI_LFS/Release_Candidates/LRC/"
	"""
	def __init__(self,config_file):
		self.config_info = get_all_config(config_file)
		print self.config_info
		self.lib_path = self.config_info["PATH"]["lib_path"]
		self.libs = os.listdir(self.lib_path)

	def remove_branch(self,branch_name):
		pass

	def add_branch(self,branch_name,value=10,option="MAX_STORE_LIBS"):
		pass

	def set_branch(self,branch_name,value,option="MAX_STORE_LIBS"):
		pass

	def manager_libs_by_branch(self,branch_name):
		try:
			if branch_name == "MAINBRANCH_LRC" :
				start_with = "MB"
				include_with = "LSP"
			else:
				start_with = "FB"
				include_with = branch_name[-4:-2]+"_"+branch_name[-2:]
			branch_libs = []
			for lib in self.libs:
				if start_with in lib and include_with in lib :
					# print start_with,include_with,lib
					branch_libs.append(lib)
			branch_libs.sort(reverse = True)
			max_num_of_libs = int(self.config_info[branch_name]["max_store_libs"])
			print branch_name,branch_libs,"branch libs number:",len(branch_libs),"max_number:",max_num_of_libs 
			if len(branch_libs) > max_num_of_libs:
				delete_libs = branch_libs[max_num_of_libs:]
			else:
				delete_libs = []
			for lib in delete_libs:
				full_name = os.path.join(self.lib_path,lib)
				print "removing lsp {0}".format(full_name)
				# os.removedirs(full_name)
			# print delete_libs
		except Exception as e:
			print  e

	def manager_all_libs(self):
		for branch in self.config_info:
			if branch is not "PATH":
				self.manager_libs_by_branch(branch)


if __name__ == '__main__':
	
	config_file = "lib_manager.conf"
	manager = LIB_MANAGER(config_file) 
	manager.manager_all_libs()
	




