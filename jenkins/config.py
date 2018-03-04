#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-29 14:25:57
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    : 
from backports.configparser import RawConfigParser

class AutoOption(object):
    def __init__(self,op):
        self.op = op

    def get_option(self):
        return self.section


class AutoSection(object):
    def __init__(self,op):
        self.op = op
        
    def get_sc(self):
        # return self.op
        return self.op.sections()

    def set_sc(self,section_dict):
        pass

    def del_sc(self):
        self.op.remove_section(section)

    section = property(get_sc,set_sc,del_sc,"new section method")


class AutoConfigParser(object):
    def __init__(self,file):
        self.op = RawConfigParser() 
        if file not in self.op.read(file):
            print "read file {0} failed".format(file)

    def get_cp(self):
        return self.op.sections()
    
    def set_cp(self,cp_dict):
        print "setting",cp_dict
        pass

    def del_cp(self):
        print "before del ...."
        print self.op.sections()
        map(self.op.remove_section,self.op.sections())
        print "after del ...."
        print self.op.sections()

    cp = property(get_cp,set_cp,del_cp,"new config parser method")


class MyConfigParser(RawConfigParser):
    def __init__(self,*args,**kwargs):
        super(MyConfigParser,self).__init__(*args, **kwargs)

    @property
    def sections(self):
        return super(MyConfigParser,self).sections()





if __name__ == '__main__':

    config = RawConfigParser()
    dict1 = {"HWAPI":{'JENKINS_URL':"http://10.140.19.16:8080/",'API_TOKEN':"7420b9fd494ed2f44cf5b7b2db9a3fe6"},
            "CCS":{'JENKINS_URL':"http://lrc-ccs-ci.china.nsn-net.net:8080/",'API_TOKEN':"e7e625aaa75399bb59a1a9707e8e787"},
            "LCP":{'JENKINS_URL':"https://lfs-lrc-ci.int.net.nokia.com/",'API_TOKEN':"d3fcf5df5939f00e1a563649e55fb664"},
            "NEW_JK":{'JENKINS_URL':"https://hzlinb49.china.nsn-net.net:8888/",'API_TOKEN':"0397240a479e3a1db848657a614d9244"}}
    config.read_dict(dict1)
    # Writing our configuration file to 'example.cfg'
    with open('jk.conf', 'wb') as configfile:
        config.write(configfile)

    lala = MyConfigParser()
    lala.read("jk.conf")
    print lala.sections
 