#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-09 16:57:11
# @Author  : robin (robin.zhu@nokia.com)
# @Description : 

from jenkins import Jenkins as JK
from jenkins import NotFoundException
import os
from os import path as PT
from my_xml import XML_FCT,save_into_file,move_file,return_file_context
import ssl,fire,json
ssl._create_default_https_context = ssl._create_unverified_context
from jenkins_cli import JK_CLI
from six.moves.urllib.request import Request
class NotFoundAPITokenError(Exception):
	"""docstring for NotFoundAPIError"""
	pass
		

api_tokens = {"http://10.140.19.16:8080/":"7420b9fd494ed2f44cf5b7b2db9a3fe6",
			"http://lrc-ccs-ci.china.nsn-net.net:8080/":"be7e625aaa75399bb59a1a9707e8e787",
			"https://lfs-lrc-ci.int.net.nokia.com/":"d3fcf5df5939f00e1a563649e55fb664",
			"https://hzlinv15.china.nsn-net.net:8080/":"af0b8e1999b644f848d8a2d13dc471a5",
			"http://hzlinb49.china.nsn-net.net:8888/":"0397240a479e3a1db848657a614d9244"
			}

VIEW_NAME = 'view/%(name)s/api/json?tree=name'

def open_new_url_with_browser(url_to_open):
	if 'LRC' in url_to_open:
		if url_to_open not in ignore_url_list:
			print "open url :",url_to_open
			os.system('"%s" %s' % (browser_path,url_to_open))
		else:
			print 'ignore url:',url_to_open
	else:
		pass
		#print url_to_open,"i guess this is not useful" 

def iteration_contain(list_object,string):
	return [i for i in list_object if string in i]

def iteration_not_contain(list_object,string):
	return [i for i in list_object if string not in i]

class MY_JK(JK):
	"""docstring for MY_JK"""
	def __init__(self,url,user_name="myselfname"):
		if url[-1] != "/":
			url = url + "/"
		host_name = [ x for x in api_tokens.keys() if x in url ]
		if host_name:
			api_token = api_tokens[host_name[0]] 
		else:
			print "plz check if url in api_tokens dict"
			raise NotFoundAPITokenError
		super(MY_JK, self).__init__(url,user_name,api_token)

		self.root_url = url

	def check_all_jobs(self):
		all_jobs = self.get_all_jobs()
		all_red_job_url = [job['url'] for job in all_jobs if job['color']=='red']
		for url in all_red_job_url:
			open_new_url_with_browser(url)

	def _get_all_views_name(self):
		try:
			view_names = [ i[u'name'] for i in  self.get_views()]
			return view_names
		except Exception as e:
			print e
			return []

	def _get_jobs_by_view(self,view_name):
		try:
			view_jobs = [ i[u"fullname"] for i in  self._get_view_jobs(view_name) ]
			return view_jobs
		except Exception as e:
			print "view_name:{0} not found on jenkins".format(view_name),e
			return []

	def save_job_config(self,job_name,path,save_shell=False):
		#save job comfig with xml format
		try:
			if not PT.exists(path):
				os.makedirs(path)
			config_xml = self.get_job_config(job_name)
			file_name = PT.join(path,job_name+".xml")
			save_into_file(file_name,config_xml)
			print "save {0} done".format(job_name)
			if save_shell:
				XML_FCT(file_name).save_xml_shell()
			#process promotions
			try:
				promotes = self.get_promotions(job_name)
				for promote in [ promote[u"name"] for promote in promotes ]:
					xml_data = self.get_promotion_config(promote,job_name)
					xml_file = PT.join(path,job_name+"__"+promote+".xml")
					save_into_file(xml_file,xml_data)
					print "save {0} config".format(promote)
			except NotFoundException as e:
				pass

		except Exception as e:
			print e

	def _reconfig_job(self,job_name,xml_file):
		print "configing",job_name,"."*30
		context = return_file_context(xml_file)
		if "__"  in job_name:
			print "i guess this is a promotion {0},please use _reconfig_promotion instead of _reconfig_job ".format(job_name)
		else:
			self.reconfig_job(job_name,context)
		#process promotions
		# try:
		# 	promotes = self.get_promotions(job_name)
		# 	for promote in [ promote[u"name"] for promote in promotes ]:
		# 		promote_file = xml_file[:-4]+"__"+promote+".xml"
		# 		xml_data = return_file_context(promote_file)
		# 		print "reconfig promote:{0}".format(promote)
		# 		self.reconfig_promotion(promote,job_name,xml_data)
		# except NotFoundException as e:
		# 	print "error:{0}in _reconfig_job {1}".format(e,xml_file)

		print "config done"

	def _create_job(self,job_name,xml_file):
		print "create",job_name,"."*30
		context = return_file_context(xml_file)
		if "__"  in job_name:
			print "i guess this is a promotion {0},please use _create_promotion instead of _create_job ".format(job_name)
		else:
			self.create_job(job_name,context)
			print "create done"

	def _reconfig_promotion(self, name, job_name, xml_file):
		print "configing promotion",job_name,"."*30
		context = return_file_context(xml_file)
		self.reconfig_promotion(name,job_name,context)

	def _create_promotion(self, name, job_name, xml_file):
		print "create promotion",job_name,"."*30
		context = return_file_context(xml_file)
		self.create_promotion(name,job_name,context)

	def reconfig_view_jobs(self,view_name,view_path):
		jobs = iteration_not_contain(self._get_jobs_by_view(view_name),"sct")
		for job in jobs:
			xml_file = os.path.join(view_path,job+".xml")
			if PT.exists(xml_file):
				self._reconfig_job(job,xml_file)
			else:
				print xml_file,"not existing"

	def save_view_jobs(self,root_path,view_name,save_shell=False,jobs_filter="Test"):
		root_path = PT.join(root_path,view_name)
		jobs = self._get_jobs_by_view(view_name)
		if jobs_filter:
			jobs = [job  for job in jobs if jobs_filter not in job]
		for job in jobs:
			self.save_job_config(job,root_path,save_shell)
		if save_shell:
			move_file(root_path,PT.join(root_path,"shell"),".sh")

	def get_description(job_name,build_number):
		return self.get_build_info(job_name,build_number)[u"description"]

	def reconfig_description(job_name,build_number,descriptions):
		"""
		descriptions line feed with <br>
		"""
		server_cli = JK_CLI(self.root_url)
		return server_cli.set_description(job_name,build_number,descriptions)

	# def view_exists(self, name):
	# 	'''Check whether a view exists

	# 	:param name: Name of Jenkins view, ``str``
	# 	:returns: ``True`` if Jenkins view exists
	# 	'''

	# 	if self.get_view_name(name):
	# 		return True

	# def get_view_name(self, name):
	# 	'''Return the name of a view using the API.

	# 	That is roughly an identity method which can be used to quickly verify
	# 	a view exists or is accessible without causing too much stress on the
	# 	server side.

	# 	:param name: View name, ``str``
	# 	:returns: Name of view or None
	# 	'''
	# 	try:
	# 		print self._build_url(VIEW_NAME, locals())
	# 		response = self.jenkins_open(Request(
	# 			self._build_url(VIEW_NAME, locals())))
	# 	except NotFoundException as e:
	# 		print e
	# 		return None
	# 	else:
	# 		actual = json.loads(response)['name']
	# 		print actual,name
	# 		if actual not in  name:
	# 			raise JenkinsException(
	# 				'Jenkins returned an unexpected view name %s '
	# 				'(expected: %s)' % (actual, name))
	# 		return actual



if __name__ == '__main__':
	root_path = "D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\hwapi"
	root_url = "http://10.140.19.16:8080/view/HWAPI_LRC/"
	server = MY_JK(root_url)
	jobs = server._get_jobs_by_view("HZSCM_TEST")
	map(server.enable_job,jobs)

	# server._create_job("PS_Release_Promo_FBLRC1613","D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\hwapi\\HWAPI_LRC\\view\\FBLRC1613\\PS_Release_Promo_FBLRC1613.xml")

	# server.create_job("EM_BM_LSP",return_file_context("D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\hwapi\\HWAPI_LRC\\view\\MAINBRANCH_LRC\\EM_BM_LSP.xml"))
	# server._create_job("PS_Release_Promo_FBLRC1613__MCU_TEST_ACCEPTED","D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\hwapi\\HWAPI_LRC\\view\\FBLRC1613\\PS_Release_Promo_FBLRC1613__MCU_TEST_ACCEPTED.xml")
	# print server.get_job_info("MCU_Build_Promo_MAINBRANCH_LRC")["downstreamProjects"]
	# print server.get_job_info("MCU_Build_Store_Libraries_MAINBRANCH_LRC")["upstreamProjects"]
	# print server._get_jobs_by_view("HWAPI_LRC/view/MAINBRANCH_LRC")
	# print server.view_exists("HWAPI_FBLRC1611")
	# print dir(server)
	# server.debug_job_info("aaa")
	# print server.get_promotion_config("PS_Promote","PS_Release_Promo_FBLRC1701")
	# server.save_view_jobs(root_path,"HWAPI_FBLRC1611",True,"Test")
	# server.save_view_jobs(root_path,"HWAPI_FBLRC1701",False,"Test")

