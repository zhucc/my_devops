import jenkins,os,shutil
import ssl,time
ssl._create_default_https_context = ssl._create_unverified_context

from xml.etree import ElementTree as ET

browser_path = "C:\Program Files (x86)\UCBrowser\Application\UCBrowser.exe"
ignore_url_list = ['https://lfs-lrc-ci.int.net.nokia.com/job/LFS_BRANCHING_-_createBranch_-_LRC/',]

"""do not use proxy"""

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

def save_into_file(filename,context):
	fp = open(filename,"w")
	fp.writelines(context)
	fp.close()

def read_file(filename):
	fp = open(filename,"r")
	return fp.read()

def check_all_url(urls):
	for url in urls:
		check_instance = MY_JENKINS(url)
		check_instance.check_all_jobs()

def get_shells(filename):
	path,name = os.path.split(filename)
	path = os.path.join(path,"shell")
	newname=name[:-4] +"_*.sh"
	shells = []
	for i in range(100):
		filename = os.path.join(path,newname.replace("*",str(i)))
		if not os.path.exists(filename):
			break
		else:
			shells.append(filename)
	return shells



class MY_JENKINS():
	"""open a jenkins url and return fp """
	def __init__(self, root_url):
		try:
			self.server = jenkins.Jenkins(root_url, username='myselfname',
			password='31393839303630317a48'.decode('hex'))
		except Exception as e:
			print e
		
	def _get_op(self):
		return self.server

	def check_all_jobs(self):
		all_jobs = self.server.get_all_jobs()
		all_red_job_url = [job['url'] for job in all_jobs if job['color']=='red']
		for url in all_red_job_url:
			open_new_url_with_browser(url)

	def _get_all_views(self):
		try:
			view_names = [ i[u'name'] for i in  self.server.get_views()]
			return view_names
		except Exception as e:
			print e
			return []

	def _get_jobs_by_view(self,view_name):
		try:
			view_jobs = [ i[u"fullname"] for i in  self.server._get_view_jobs(view_name) ]
			return view_jobs
		except Exception as e:
			print e
			return []

	def disable_jobs(self):
		try:
			view_names = self._get_all_views()
			LRC_view_names = [i for i in view_names if u'FBLRC' in i]
			for view in LRC_view_names:
				all_view_jobs = self._get_jobs_by_view(view)
				test_jobs = [i for i in all_view_jobs if u"Test" in i]
			for job in test_jobs:
				self.server.disable_job(job)
			return True	
		except Exception as e:
			print e
			return False
	
	def get_config_by_jobname(self,jobname):
		# return xml configuration
		try:
			return self.server.get_job_config(jobname)
		except Exception as e:
			print e
			return None

	def save_job_config(self,jobname,path,save_shell=True):
		#save job comfig with xml format
		try:
			config_xml = self.get_config_by_jobname(jobname)
			filename = os.path.join(path,jobname+".xml")
			save_into_file(filename,config_xml)
			if save_shell:
				self.save_shell_scripts(filename)
		except Exception as e:
			print e

	def reconfig_job(self,jobname,xmlfile):
		print "configing",jobname,"."*30
		context = read_file(xmlfile)
		self.server.reconfig_job(jobname,context)
		print "config done"

	def reconfig_view_jobs(self,view_name,xmlpath):
		jobs = [i for i in self._get_jobs_by_view(view_name) if "Test" not in i]
		for job in jobs:
			xmlfile = os.path.join(xmlpath,job+".xml")
			if os.path.exists(xmlfile):
				self.reconfig_job(job,xmlfile)
			else:
				print xmlfile,"not existing"


	def save_shell_scripts(self,xmlname):
		tree = ET.parse(xmlname)
		root = tree.getroot()
		command_elements = [i for i in root.iter("command")]
		#finish get all shell operator list:command_elements
		#save it's context
		for index,ce in enumerate(command_elements):
			filename = xmlname[:-4] + '_' + str(index) + ".sh" 

			directory,name = os.path.split(filename)
			if not os.path.exists(directory+"\\shell"):
				os.mkdir(directory+"\\shell")
			new_filename = os.path.join(directory+'\\shell',name)
			save_into_file(new_filename,ce.text)	

	def save_view_jobs_shell(self,view_name,path2save):
		jobs = [ i for i in self._get_jobs_by_view(view_name) if "Test" not in i ]
		for job in jobs:
			self.save_job_config(job,path2save)

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
	
	def modify_xml_shell(self,shell_files):
		'''
		shell_files: list of file
		'''
		elements = self.get_elements("command")
		for index,ce in enumerate(elements):
			#print "change shell script {0} in {1}".format(index,self.xmlname)
			ce.text=read_file(shell_files[index])
		self.tree.write(self.xmlname)

	def modify_xml_build_node(self,node_name):
		elements =self.get_elements("assignedNode")
		for index,ce in enumerate(elements):
			#print "change node {0} in {1}".format(index,self.xmlname)
			ce.text=node_name
		self.tree.write(self.xmlname)


	def modify_a_xml(self):
		new_scripts = get_shells(self.xmlname)
		self.modify_xml_shell(new_scripts)
		self.modify_xml_build_node("build")

class TOP_FUNCTION():
	
	def __init__(self,jenkins_url,rootpath):
		self.server = MY_JENKINS(jenkins_url)
		self.views = ["HWAPI_FBLRC1512","HWAPI_FBLRC1611","HWAPI_FBLRC1606","HWAPI_FBLRC1701"]
		self.branchs = [view.split("_")[-1] for view in self.views]
		self.branchs.append("MAINBRANCH_LRC")
		self.branch_paths = []
		for branch in self.branchs:
			branch_path = os.path.join(rootpath,branch)
			if  not os.path.exists(branch_path):
				os.mkdir(branch_path)
			self.branch_paths.append(branch_path)

	def _get_path_according_view(self,view_name):
		if view_name == "HWAPI_MAINBRANCH_LRC":
			return [i for i in self.branch_paths if 'MAINBRANCH_LRC' in i ][0]
		path2save = [path for path in self.branch_paths if view_name.split("_")[-1] in path]
		if len(path2save) == 1:
			return path2save[0]
		else:
			print path2save,"error dir"
			return None

	def save_view_jobs_config(self,view_name):
		'''
		path = "D:\\userdata\\myselfname\\Desktop\\FBLRC1611"
		save jobs xml amd shell in to path2save
		'''
		path = self._get_path_according_view(view_name)
		if path is not None:	
			print "save_jobs_config of {0}".format(view_name)	
			self.server.save_view_jobs_shell(view_name,path)
			print "done"
	
	def modify_local_shells(self,src_view,dst_view):
		'''
		cp src shell scripts to dst
		dst_path = "D:\\userdata\\myselfname\\Desktop\\FBLRC1606"
		'''
		dst_branch = dst_view.split("_")[-1]
		src_branch = src_view.split("_")[-1]
		dst_path = self._get_path_according_view(dst_view)
		if dst_path is not None:	
			print "use {0} shells to cover {1} shell".format(src_branch,dst_branch)	
			for root,dirs,files in os.walk(dst_path+"\\shell"):
				for file in files:
					dst_file = os.path.join(root,file)
					src_file = dst_file.replace(dst_branch,src_branch)
					if os.path.exists(src_file):
						shutil.copyfile(src_file,dst_file)
					else:
						print src_file,"not exists....."
			print "done"

	def modify_all_xml(self,view_name):
		'''
		modify all xml file in xmlpath according to local shell
		xmlpath = "D:\\userdata\\myselfname\\Desktop\\FBLRC1606"
		'''
		branch_path = self._get_path_according_view(view_name)
		if branch_path is not None:	
			print "modify all xml files in",branch_path	
			scm_job_xmls = []
			for root,dirs,files in os.walk(branch_path):
				for file in files:
					if os.path.splitext(file)[1] == '.xml':
						scm_job_xmls.append( os.path.join(root,file) )
			for fullname in scm_job_xmls:
				xml_op = XML_FCT(fullname)
				xml_op.modify_a_xml()
			print "done"

	def reconfig_jobs_with_loacl_xml(self,view_name):
		'''
		xmlpath = "D:\\userdata\\myselfname\\Desktop\\FBLRC1606"
		'''
		branch_path = self._get_path_according_view(view_name)
		if branch_path is not None:	
			print "reconfig jobs in {0} with loaclxml".format(view_name)
			self.server.reconfig_view_jobs(view_name,branch_path)
			print "done"



def exampel_test():
	# exp1=0
	# root_url = ['https://lfs-lrc-ci.int.net.nokia.com/',]
	# while  True:
	# 	check_one.check_all_url(root_url)
	# 	time.sleep(10*60)

	# exp2=0
	# urls = ['https://lfs-lrc-ci.int.net.nokia.com/','https://hzlinv15.china.nsn-net.net:8080/',
	# 	'http://lrc-ccs-ci.china.nsn-net.net:8080/']
	# check_all_url(urls)
	
	# exp3="save 1611 shell scripts"
	# server = MY_JENKINS('http://10.140.19.16:8080/')
	# path2save = "D:\\userdata\\myselfname\\Desktop\\FBLRC1611"
	# server.save_view_jobs_shell("HWAPI_FBLRC1611",path2save)

	# exp3="save 1606 shell scripts"
	# server = MY_JENKINS('http://10.140.19.16:8080/')
	# path2save = "D:\\userdata\\myselfname\\Desktop\\FBLRC1606"
	# server.save_view_jobs_shell("HWAPI_FBLRC1606",path2save)

	# exp4="cp 1611 shell scripts to 1606"
	# path2save = "D:\\userdata\\myselfname\\Desktop\\FBLRC1606"
	# for root,dirs,files in os.walk(path2save+"\\shell"):
	# 	for file in files:
	# 		dst_file = os.path.join(root,file)
			
	# 		src_file = dst_file.replace("FBLRC1606","FBLRC1611")
	# 		if os.path.exists(src_file):
	# 			shutil.copyfile(src_file,dst_file)
	# 		else:
	# 			print src_file,"not existing"

	# exp5-1="modify shell part in xml of DSP_Build_RT_FBLRC1606 with 1606 shell scripts "
	# filename = "D:\\userdata\\myselfname\\Desktop\\FBLRC1606\\DSP_Build_RT_FBLRC1606.xml"
	# xml_op = XML_FCT(filename)
	# xml_op.modify_a_xml()

	# exp5="modify xml of all jobs in a path "
	# xmlpath = "D:\\userdata\\myselfname\\Desktop\\FBLRC1606"
	# scm_job_xmls = []
	# for root,dirs,files in os.walk(xmlpath):
	# 	for file in files:
	# 		if os.path.splitext(file)[1] == '.xml':
	# 			scm_job_xmls.append( os.path.join(root,file) )
	# for fullname in scm_job_xmls:
	# 	xml_op = XML_FCT(fullname)
	# 	xml_op.modify_a_xml()

	# exp6="reconfig view jobs with *.xml in xmlpath"
	# xmlpath = "D:\\userdata\\myselfname\\Desktop\\FBLRC1606"
	# server = MY_JENKINS('http://10.140.19.16:8080/')
	# server.reconfig_view_jobs("HWAPI_FBLRC1606",xmlpath)
	pass

def change_view_jobs_config(rootpath,rooturl,src_view,dst_view):
	"config all job in dst_view according to src_view "
	operator = TOP_FUNCTION(rooturl,rootpath)
	#operator.save_view_jobs_config(dst_view)
	operator.save_view_jobs_config(src_view)
	# operator.modify_local_shells(src_view,dst_view)
	# operator.modify_all_xml(dst_view)
	# operator.reconfig_jobs_with_loacl_xml(dst_view)


if __name__ == '__main__':
	print "hahaha"
	# exp1=0
	# root_url = ['https://lfs-lrc-ci.int.net.nokia.com/',]
	# while  True:
	# 	check_one.check_all_url(root_url)
	# 	time.sleep(10*60)

	# rootpath = "D:\\test"
	# rooturl = "http://10.140.19.16:8080/"
	# change_view_jobs_config(rootpath,rooturl,"HWAPI_MAINBRANCH_LRC","HWAPI_FBLRC1606")

	# server = MY_JENKINS("http://lrc-ccs-ci.china.nsn-net.net:8080")._get_op()
	# print dir(server)
	# server.get_build_info("FBLRC1606_test.trigger",7)[u"description"] 
	
	