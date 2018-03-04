#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-10 11:20:20
# @Author  : robin (robin.zhu@nokia.com)
# @Description : 

from xml.etree import ElementTree as ET
from os import path as PT
import os,shutil

def return_file_context(filename):
		with open(filename,"r") as fp:
			return fp.read()
			
def return_file_contexts(filename):
		with open(filename,"r") as fp:
			return fp.readlines()

def save_into_file(filename,context):
	with open(filename,"w") as fp:
		fp.writelines(context)

def move_file(src_path,dst_path,filter_string):
	"""
	move_file("D:\\test_ccs\\MAINBRANCH_LRC","D:\\test_ccs\\MAINBRANCH_LRC\\shell",".sh")

	"""
	if not PT.exists(dst_path):
		os.makedirs(dst_path)
	for root,dirs,files in os.walk(src_path):
		for file in files:
			if filter_string in file:
				src_file = PT.join(root,file) 
				dst_file = PT.join(dst_path,file) 
				shutil.move(src_file,dst_file)


def get_shells(xml_file):
	file_path,file_name = PT.split(xml_file)
	shell_path = PT.join(file_path,"shell")
	shell_files = []
	for i in range(100):
		shell_name =file_name[:-4] + "_" +str(i) +".sh"
		shell_file = PT.join(shell_path,shell_name)
		if PT.exists(shell_file):
			shell_files.append(shell_file)
		else:
			break
	return shell_files

class XML_FCT():
	"""factory of processing XML"""
	def __init__(self, xmlname):
		self.xmlname = xmlname
		self.tree = ET.parse(xmlname)
		self.root = self.tree.getroot()
		
	def get_elements(self,element_name):
		command_elements = [i for i in self.root.iter(element_name)]
		return command_elements

	def save_xml_shell(self):
		elements = self.get_elements("command")
		for index,ce in enumerate(elements):
			filename = self.xmlname[:-4] + '_' + str(index) + ".sh" 
			save_into_file(filename,ce.text)

	def modify_xml_build_node(self,node_name):
		elements = self.get_elements("assignedNode")
		for index,ce in enumerate(elements):
			#print "change node {0} in {1}".format(index,self.xmlname)
			ce.text=node_name
		self.tree.write(self.xmlname)

	def modify_xml_shell(self,shell_files):
		'''
		shell_files: list of file
		'''
		try:
			elements = self.get_elements("command")
			for index,ce in enumerate(elements):
				#print "change shell script {0} in {1}".format(index,self.xmlname)
				ce.text=return_file_context(shell_files[index])
			self.tree.write(self.xmlname)
		except IndexError:
			print "{0} has more command part than local shells ".format(self.xmlname)
			
	def modify_a_xml(self):
		new_scripts = get_shells(self.xmlname)
		print "modify xml file at {0}".format(self.xmlname)
		self.modify_xml_shell(new_scripts)
		self.modify_xml_build_node("build")

	def replace_a_xml(self,original,present):
		for element in self.root.iter():
			if element.text is not None and original in element.text:
				#print element,self.xmlname
				element.text = element.text.replace(original,present)
		self.tree.write(self.xmlname)

	def add_email(self,email_address="I_MN_P_BBP_SCM_HZ_PS@internal.nsn.com"):
		mail_element = ET.Element("hudson.tasks.Mailer")
		mail_element.set("plugin","mailer@1.17")
		a_element = ET.Element("recipients")
		a_element.text = email_address
		b_element = ET.Element("dontNotifyEveryUnstableBuild")
		b_element.text = 'false'
		c_element = ET.Element("sendToIndividuals")
		c_element.text = 'false'
		mail_element.append(a_element)
		mail_element.append(b_element)
		mail_element.append(c_element)
		for element in self.root.iterfind("publishers"):
			if not element.iterfind("Mailer"):
				element.append(mail_element)
		self.tree.write(self.xmlname)

	def get_sub_build_projects(self):
		element =  self.get_elements("builders")[0]
		result = ",".join([ i.text.replace(" ","" ) for i in  element.iter("projects")]).split(",")
		if result == ['']:
			result = []
		return result

	def get_scm(self):
		for element in self.get_elements("scm"):
			return [ i.text.strip() for i in element.iter("remote")]

if __name__ == '__main__':
	
	op = XML_FCT("job_config_file")
	# print op.root.getchildren()
	aa = op.get_sub_build_projects()
	print aa
	print return_file_context("D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\hwapi\\HWAPI_LRC\\view\\FBLRC1613\\PS_Release_Promo_FBLRC1613__MCU_TEST_ACCEPTED.xml")
	# print op.get_sub_build_projects()
	# for element in  op.get_elements("builders"):
	# 	print element
	# 	print [i for i in element.iter("projects")]
		# print element.getchildren()[1].getchildren()[0].getchildren()