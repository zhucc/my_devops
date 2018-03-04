#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-19 17:11:23
# @Author  : robin (robin.zhu@nokia.com)

import os,json,sys
def get_currentPatchSet_number(file_name):
    try:
        with open(file_name,'r') as f:
            data = json.load(f)
            # for key,value in data.items():
                # print "{0} >>>>>>{1}".format(key,value)
            print data["currentPatchSet"]["number"]
    except Exception as e:
        print e

def get_some_key(file_name,*key_names):
    try:
        with open(file_name,'r') as f:
            data = json.load(f)
            
            # for key,value in data.items():
                # print "{0} >>>>>>{1}".format(key,value)
            # print key_names,type(key_names)
            return iteration_multi_dict(data,key_names)
    except Exception as e:
        raise e
        return 1

def iteration_multi_dict(multi_dict,*key_names):
    key_lists = []
    # key_names = key_names[0]
    for key,value in multi_dict.items():
        print key,key_names,type(key_names)
        if key == key_names[0][0]:
            print "key >>>>{0}".format(key)
            
            key_lists = key_lists  +  [{key,value}]
            key_names = key_names[0][1:]
    return key_lists






if __name__ == '__main__':
    # file_name = sys.argv[1]
    # get_currentPatchSet_number(file_name)
    print get_some_key("aa.json","currentPatchSet","number")
