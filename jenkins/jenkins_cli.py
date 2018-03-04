#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-09 21:53:39
# @Author  : robin (robin.zhu@nokia.com)
# @Description : 

import urllib2,commands
from os import path as PT
from os import getenv
# need config ssh pub key in jenkins
def excute_shell(cmd_string):
    print cmd_string
    return commands.getoutput(cmd_string)


class JK_CLI():
    """
    python class for jenkins cli for set description
    """
    def __init__(self,url):
        now_path = PT.abspath(".")
        self.jar_file = PT.join(now_path,"jenkins-cli.jar")
        self.url = url
        if not PT.exists(self.jar_file):
            f = urllib2.urlopen(url+"/jnlpJars/jenkins-cli.jar")
            with open("jenkins-cli.jar","wb") as jarlib:
                jarlib.write(f.read())

    def set_description(self,job_name,build_number,descriptions):
        cmd = "java -jar {0} -auth {5}:{6} -s {1} set-build-description {2} {3} {4}".format(self.jar_file,self.url,job_name,build_number,descriptions,user,apitoken)
        return excute_shell(cmd)


if __name__ == '__main__':
    JENKINS_URL = getenv("JENKINS_URL")
    JOB_NAME = getenv("JOB_NAME")
    BUILD_NUMBER = getenv("BUILD_NUMBER")
    GERRIT_CHANGE_NUMBER = getenv("GERRIT_CHANGE_NUMBER")
    GERRIT_PATCHSET_NUMBER = getenv("GERRIT_PATCHSET_NUMBER")
    GERRIT_PROJECT = getenv("GERRIT_PROJECT")
    print JENKINS_URL,JOB_NAME,BUILD_NUMBER,GERRIT_CHANGE_NUMBER,GERRIT_PATCHSET_NUMBER,GERRIT_PROJECT
    server = JK_CLI(JENKINS_URL)
    description = GERRIT_PROJECT+","+GERRIT_CHANGE_NUMBER+","+GERRIT_PATCHSET_NUMBER
    print server.set_description(JOB_NAME,BUILD_NUMBER,description)



