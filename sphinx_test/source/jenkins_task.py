# import shutil,os
# from my_jenkins import MY_JK
# from my_xml import XML_FCT,save_into_file
# from os import path as PT
# import fire

"""do not use proxy"""



class JK_FUNCTION():
	
	def __init__(self,jenkins_url,rootpath):
		self.server = MY_JK(jenkins_url)
		self.rootpath = rootpath
		self.view_paths = {}
		self.job_config_xmls = {}
		
	def _get_path_according_view(self,view_name):
		if not self.view_paths.has_key(view_name):
			view_path =  PT.join(self.rootpath,view_name.replace("/","\\"))
			if not PT.exists(view_path):
				os.makedirs(view_path)
			self.view_paths[view_name] = view_path
		return self.view_paths[view_name]

	def save_view_jobs_config(self,view_name,save_shell=False,jobs_filter = "Test"):
		self.server.save_view_jobs(self.rootpath,view_name,save_shell,jobs_filter)

	def modify_all_xml(self,view_name):
		'''
		modify all xml file in xmlpath according to local shell
		'''
		branch_path = self._get_path_according_view(view_name)
		if branch_path is not None:	
			print "modify all xml files in",branch_path	
			scm_job_xmls = []
			for root,dirs,files in os.walk(branch_path):
				for file in files:
					if PT.splitext(file)[1] == '.xml':
						scm_job_xmls.append( PT.join(root,file) )
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

	def cp_src_xmls_2_dst(self,src_view,dst_view):
		src_view_path = self._get_path_according_view(src_view)
		dst_view_path = PT.join(self.rootpath,dst_view)
		if PT.exists(dst_view_path):
			shutil.rmtree(dst_view_path)
		shutil.copytree(src_view_path,dst_view_path)

	def replace_view_xmls(self,view_name,original,present):
		"""
		replace all original string in view_name with present string
		"""
		view_path = self._get_path_according_view(view_name)
		for root,dirs,files in os.walk(view_path):
			for file in files:
				if file[-3:] == 'xml':
					old_file = PT.join(root,file)
					new_file = PT.join(view_path,file.replace(original,present))
					#print old_file,">>"*10,new_file
					os.rename(old_file,new_file)
					
					self.job_config_xmls[file.replace(original,present)[:-4]] = new_file

		for file in self.job_config_xmls.values():
			xml_op = XML_FCT(file)
			xml_op.replace_a_xml(original,present)

	def create_all_jobs(self):
		for job_name,job_xml in self.job_config_xmls.items():
			is_promotion = ("__" in job_name)
			if is_promotion:
				continue
			print "try to create {0}".format(job_name)
			if not self.server.job_exists(job_name):
				print "create {0} job with local xml at {1}".format(job_name,job_xml)
				self.server._create_job(job_name,job_xml)
			elif self.server.job_exists(job_name):
				print "reconfig {0} job with local xml at {1}".format(job_name,job_xml)
				self.server._reconfig_job(job_name,job_xml)
			else:
				pass
			try:
				self.server.disable_job(job_name)
			except Exception as e:
				print e

	def create_all_promotions(self):
		for job,job_xml in self.job_config_xmls.items():
			is_promotion = ("__" in job)
			if is_promotion:
				job_name,name =  job.split("__")
				print name,job_name,job_xml
				if self.server.promotion_exists(name,job_name):
					self.server._reconfig_promotion(name,job_name,job_xml)
				else:
					self.server._create_promotion(name,job_name,job_xml)
			else:
				pass
				
	def create_view_with_model_view_and_add_jobs(self,model_view_name,new_view_name,original,present):
		"""
			get model view xml
			replace original in xml with present
			create new view with new xml
		"""
		print model_view_name,new_view_name
		if self.server.view_exists(model_view_name):

			model_xml = self.server.get_view_config(model_view_name)
			model_xml = model_xml.replace(original,present)
			save_into_file(PT.join(self.rootpath,model_view_name+".xml"),model_xml)
			if not self.server.view_exists(new_view_name):
				print "creating view ...."
				self.server.create_view(new_view_name,model_xml)
			else:
				print "reconfiging view ...."
				self.server.reconfig_view(new_view_name,model_xml)

		else:
			print "can not find model view {0}".format(model_view_name)

	def add_email_2jobs_in(self,view_name):
		all_jobs = self.server._get_jobs_by_view(view_name)
		filter_job_result = [i for i in all_jobs if "trigger" in i or "builder" in i or "promo" in i ]
		for job in filter_job_result:
			xmlpath = PT.join(self.rootpath + "\\" + view_name , job + ".xml")
			XML_FCT(xmlpath).add_email()
			print "add email to {0} done".format(job)
			#self.server.reconfig_job(job,xmlpath)

	def analyse_view_jobs(self,view_name):
		job_relationships = {}
		jobs = self.server._get_jobs_by_view(view_name)
		for job in jobs:
			job_relationships[job] = self.analyse_one_job(job)
		return job_relationships

	def analyse_one_job(self,job_name):
		job_info = self.server.get_job_info(job_name)
		tmp = {}
		tmp["jobName"] = job_name
		tmp["upstreamProjects"] = [ i["name"] for i in job_info["upstreamProjects"] ]
		tmp["downstreamProjects"] = [ i["name"] for i in job_info["downstreamProjects"] ]
		job_config_xml = self.server.get_job_config(job_name)
		# print job_config_xml
		save_into_file("job_config_file",job_config_xml)
		file_op = XML_FCT("job_config_file")
		sub_builds = file_op.get_sub_build_projects()
		scm = file_op.get_scm()
		tmp["subBuilds"] = sub_builds
		tmp["scm"] = scm
		return tmp
	

def change_view_jobs_config(rootpath,rooturl,src_view,dst_view):
	"config all job in dst_view according to src_view "
	operator = JK_FUNCTION(rooturl,rootpath)
	operator.save_view_jobs_config(src_view)
	operator.save_view_jobs_config(dst_view)
	operator.modify_all_xml(dst_view)
	operator.reconfig_jobs_with_loacl_xml(dst_view)




class branch_object(object):

	def make_a_branch(self,root_path,root_url,src_view,dst_view,src_branch,dst_branch,replace_list):
		"""
		usage:make_a_branch(root_path,root_url,"MAINBRANCH_LRC","FBLRC2000_TST",[(A,B),(A1,B1)])
		"""
		#replace_tuple [(origin1,replace1),(origin2,replace2)....]

		

		operator = JK_FUNCTION(root_url,root_path)
		# operator.save_view_jobs_config(src_view,jobs_filter="EM_BM_LSP")
		operator.cp_src_xmls_2_dst(src_view,dst_view)
		list(map(operator.replace_view_xmls,[dst_view for i in replace_list],[i[0] for i in replace_list],[i[1] for i in replace_list]))
		operator.create_all_jobs()
		operator.create_all_promotions()
		operator.create_view_with_model_view_and_add_jobs(src_view,dst_view,src_branch,dst_branch)



if __name__ == '__main__':

	root_path = "D:\\userdata\\myselfname\\Desktop\\work_script\\jenkins_job_config\\hwapi"
	root_url = "http://10.140.19.16:8080/view/HWAPI_LRC/"
	lala = branch_object()
	lala.make_a_branch(root_path,root_url,"MAINBRANCH_LRC","HZSCM_TEST","MAINBRANCH_LRC","HZSCM_TEST",[("MAINBRANCH_LRC","HZSCM_TEST")])
	# huahua = JK_FUNCTION(root_url,root_path)
	# print huahua.analyse_one_job("DSP_Build_Promo_MAINBRANCH_LRC")
	# fire.Fire(branch_object)



		
