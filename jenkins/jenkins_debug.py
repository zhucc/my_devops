#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-20 11:04:03
# @Author  : robin (robin.zhu@nokia.com)
# @Description : 
import shutil,os
from  jenkins import NotFoundException
from my_jenkins import MY_JK
from my_xml import XML_FCT,save_into_file,return_file_contexts,return_file_context
from os import path as PT
from jenkins_task import JK_FUNCTION
from jenkins import EMPTY_CONFIG_XML
"""
jenkins_functions 
'__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', 
'__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', 
'__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
'_add_missing_builds', '_build_url', '_create_job', '_get_all_views_name', 
'_get_encoded_params', '_get_job_folder', '_get_jobs_by_view', '_get_view_jobs', 
'_reconfig_job', 'assert_job_exists', 'assert_node_exists', 'assert_promotion_exists', 
'assert_view_exists', 'auth', 'build_job', 'build_job_url', 'cancel_queue', 
'check_all_jobs', 'copy_job', 'create_job', 'create_node', 'create_promotion', 
'create_view', 'crumb', 'debug_job_info', 'delete_job', 'delete_node', 'delete_promotion', 
'delete_view', 'disable_job', 'disable_node', 'enable_job', 'enable_node', 'get_all_jobs', 
'get_build_console_output', 'get_build_info', 'get_info', 'get_job_config', 'get_job_info', 
'get_job_info_regex', 'get_job_name', 'get_jobs', 'get_node_config', 'get_node_info', 
'get_nodes', 'get_plugin_info', 'get_plugins', 'get_plugins_info', 'get_promotion_config', 
'get_promotion_name', 'get_promotions', 'get_promotions_info', 'get_queue_info', 
'get_running_builds', 'get_version', 'get_view_config', 'get_view_name', 'get_views', 
'get_whoami', 'install_plugin', 'jenkins_open', 'job_exists', 'jobs_count', 
'maybe_add_crumb', 'node_exists', 'promotion_exists', 'quiet_down', 'reconfig_job', 
'reconfig_node', 'reconfig_promotion', 'reconfig_view', 'reconfig_view_jobs', 
'rename_job', 'root_url', 'run_script', 'save_job_config', 'save_view_jobs', 'server', 
'set_next_build_number', 'stop_build', 'timeout', 'view_exists']
"""
def main():
	root_path = "D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\hwapi"
	root_url = "http://10.140.19.16:8080/"
	server = MY_JK(root_url)
	# print server.view_exists("HWAPI_FBLRC1611")
	# server.save_view_jobs(root_path,"HWAPI_FBLRC1611",False,"Test")


	server.save_view_jobs(root_path,"HWAPI_FBLRC1701",False,"Test")
	# server.save_view_jobs(root_path,"HWAPI_MAINBRANCH_LRC",False,False)
	# shell_path = PT.join(root_path,"HWAPI_FBLRC1701\\shell")
	# # shutil.copytree(PT.join(root_path,"HWAPI_FBLRC1611\\shell"),shell_path)
	# # for root,dirs,files in os.walk(shell_path):
	# # 	for file in files:
	# # 		new_name = file.replace("1611","1701")
	# # 		os.rename(PT.join(root,file),PT.join(root,new_name))
	# xml_dict = {}
	# for root,dirs,files in os.walk(PT.join(root_path,"HWAPI_FBLRC1611")):
	# 	for file in files :
	# 		if file[-4:] == ".xml":
	# 			xml_file = PT.join(root,file)
	# 			#XML_FCT(xml_file).modify_a_xml()
	# 			xml_dict[file[:-4]] = xml_file
	# print xml_dict
	# for job_name,xml_file in xml_dict.items():
	# 	print job_name,xml_file
	# 	server._reconfig_job(job_name,xml_file)

def hwapi_debug():
	root_path = "D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\hwapi"
	root_url = "http://10.140.19.16:8080/"
	server = JK_FUNCTION(root_url,root_path)
	jk_server = server.server

	# jobs = jk_server._get_jobs_by_view("HWAPI_LRC/view/FBLRC1611/")
	# for job in jobs:
	# 	if "Test" not in job:
	# 		print job
	# 		jk_server.enable_job(job)
	# print root_path
	# print PT.join(root_path ,"HWAPI_LRC\\view\\FBLRC1611")
	# for root,dirs,files in os.walk(PT.join(root_path,"HWAPI_LRC\\view\\FBLRC1701")):
	# 	for file in files:
	# 		new_name = file.replace("FBLRC1611","FBLRC1701")
	# 		aa = PT.join(root,file)
	# 		bb = PT.join(root,new_name)
	# 		os.rename(aa,bb)
	# print PT.join(root_path,"\\HWAPI_LRC\\view\\FBLRC1701")
	# server.save_view_jobs_config("HWAPI_LRC/view/FBLRC1706/")
	server.save_view_jobs_config("HWAPI_LRC/view/MAINBRANCH_LRC/")
	server.save_view_jobs_config("HWAPI_LRC/view/GERRIT/")
	server.save_view_jobs_config("HWAPI_LRC/view/CCI_MAINBRANCH_LRC/")
	server.save_view_jobs_config("HWAPI_LRC/view/FBLRC1708/")
	# server.reconfig_jobs_with_loacl_xml("HWAPI_LRC/view/FBLRC1701/")
	# server.save_view_jobs_config("HWAPI_LRC/view/CCI_MAINBRANCH_LRC/",False,"Test")
	# for name in  jk_server._get_jobs_by_view("HWAPI_LRC/view/TEST/"):
	# 	new_name = name.replace("FBLRC1611","MAINBRANCH_LRC  ")
	# 	jk_server.rename_job(name,new_name)
	
	# for i in ["MCU_Build_LRC_ModuleTest_MAINBRANCH_LRC_TEST","MCU_Build_ObjectModel_UnitTests_LCP_MAINBRANCH_LRC_TEST","MCU_Build_ObjectModel_ModuleTests_LCP_MAINBRANCH_LRC_TEST","MCU_Build_Rel3_UnitTest_Valgrind_MAINBRANCH_LRC_TEST","MCU_Build_Rel3_UnitTest_MAINBRANCH_LRC_TEST","MCU_Build_ObjectModel_UnitTests_LSP_AXM_MAINBRANCH_LRC_TEST","MCU_Build_Rel3_LRC_MAINBRANCH_LRC_TEST", "MCU_Build_Rel3_LRC_LSP_MAINBRANCH_LRC_TEST"]:
	# 	if not jk_server.job_exists(i):
	# 		print i
	# 		jk_server.create_job(i,EMPTY_CONFIG_XML)

	# server.cp_src_xmls_2_dst("HWAPI_FBLRC1611","HWAPI_FBLRC1606")
	# server.replace_view_xmls("HWAPI_FBLRC1606","FBLRC1611","FBLRC1606")
	# server.replace_view_xmls("HWAPI_FBLRC1606","SVN_SCRIPTS_LRC","SVN_SCRIPTS_LRC_TEST")
	# server.reconfig_jobs_with_loacl_xml("HWAPI_LRC/view/TEST/")

def ccs_debug():
	root_path = "D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\ccs"
	root_url = "http://lrc-ccs-ci.china.nsn-net.net:8080/"
	server = JK_FUNCTION(root_url,root_path)
	server.save_view_jobs_config("All")
	# for root,dirs,files in os.walk(PT.join(root_path,"TEMPLATE")):
	# 	for file in files:
	# 		xml_file = PT.join(root,file)
	# 		for branch in ["MAINBRANCH_LRC","FBLRC1701","FBLRC1611","FBLRC1606"]:
	# 			job_name = file[:-4].replace("TEMPLATE", branch)
	# 			context = return_file_context(xml_file)
	# 			context = context.replace("TEMPLATE",branch)
	# 			context = context.replace("ccs_mainbranch_test","CCS_"+branch)
	# 			context = context.replace("MAINBRANCH_LRC",branch)
	# 			if not server.job_exists(job_name):
	# 				print job_name
	# 				server.create_job(job_name,context)
	# 			else:
	# 				print "reconfig:",job_name
	# 				server.reconfig_job(job_name,context)
	# 			server.disable_job(job_name)
			#server._reconfig_job(file[:-4],PT.join(root,file))


def ps_debug():
	root_path = "D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\ps"
	root_url = "https://hzlinv15.china.nsn-net.net:8080"
	server = MY_JK(root_url)
	server.save_view_jobs(root_path,"All",False,False)

def new_jenkins():
	root_path = "D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\new_jenkins"
	root_url = "http://hzlinb49.china.nsn-net.net:8888/"
	server = MY_JK(root_url)
	# server.save_view_jobs(root_path,"GERRIT",False,False)
	server._reconfig_job("LSP_Auto_Submit",PT.join(root_path,"LSP_Auto_Submit.xml"))

if __name__ == '__main__':
    # ccs_debug()
	# main()
	# ps_debug()
	# hwapi_debug()
	new_jenkins()
	# root_path = "D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\hwapi"
	# root_url = "http://10.140.19.16:8080/"
	# server = JK_FUNCTION(root_url,root_path)
	# jk_server = server.server
	# print "aaaa"
	# for root,dirs,files in os.walk("D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\hwapi\\HWAPI_LRC\\view\\CCI_MAINBRANCH_LRC"):
	# 	for file in files:
	# 		job_name = file[:-4]
	# 		print job_name
	# 		file = PT.join(root,file)
	# 		context = return_file_context(file)
	# 		jk_server.reconfig_job(job_name,context)

