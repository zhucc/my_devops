#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-29 14:25:02
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    : 

api_tokens = {"http://10.140.19.16:8080/":"7420b9fd494ed2f44cf5b7b2db9a3fe6",
			"http://lrc-ccs-ci.china.nsn-net.net:8080/":"be7e625aaa75399bb59a1a9707e8e787",
			"https://lfs-lrc-ci.int.net.nokia.com/":"d3fcf5df5939f00e1a563649e55fb664",
			"https://hzlinv15.china.nsn-net.net:8080/":"af0b8e1999b644f848d8a2d13dc471a5",
			"http://hzlinb49.china.nsn-net.net:8888/":"0397240a479e3a1db848657a614d9244"
			}

from jenkins import Jenkins as JK
from jenkins import NotFoundException
import os
from os import path as PT
import ssl,fire
ssl._create_default_https_context = ssl._create_unverified_context

def open_jenkins_with_account(jenkins_url,user_name="myselfname"):
	if jenkins_url in api_tokens :
		op = JK(jenkins_url,user_name,api_tokens[jenkins_url])
		return op
	else:
		raise SystemExit("can not find match jenkins url in api_tokens dict")
		return None

def change_one_job_status(job_url,job_status):
	try:
		job_url = job_url.strip()
		job_url = job_url[:-1] if job_url.endswith("/") else job_url
		job_name = job_url.split("/")[-1]
		for key,value in api_tokens.items():
			if  key in job_url:
				jenkins_url = key
				break
		else:
			raise SystemExit("can not find match jenkins url in api_tokens dict")
		operator = open_jenkins_with_account(jenkins_url)
		if operator is not None:
			if job_status.lower() == "enable":
				print("enable {0} ....".format(job_name))
				operator.enable_job(job_name)
			elif job_status.lower() == "disable":
				print("disable {0} ....".format(job_name))
				operator.disable_job(job_name)
			else:
				raise SystemExit("choice one from enable and disable, {job_status} is invalid ".format(job_status=job_status))
	except NotFoundException as e:
		raise SystemExit ("can not find job name {0} in jenkins {1}".format(job_name,jenkins_url))
	except Exception as e:
		raise e

	
def change_job_status(jobs_url,job_status):
	jobs =jobs_url.split(",")
	list(map(change_one_job_status,jobs,[job_status for i in range(len(jobs))] ))


if __name__ == '__main__':
	job_url = "http://lrc-ccs-ci.china.nsn-net.net:8080/view/Admin/job/Submit_In_Gerrit/"
	change_job_status(job_url,"ENable")
	fire.Fire(change_job_status)