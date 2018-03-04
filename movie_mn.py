#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-25 09:13:34
# @Author  : robin (robin.zhu@nokia.com)
# @Description : 
import shutil
import os
from os.path import join, getsize

def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        print root,dirs,files
        size += sum([getsize(join(root, name)) for name in files])
    return (size/1024/1024)

def mv_file_outside(dir,filter_size=10):
    #filter_size:M
    for root,dirs,files in os.walk(dir):
        #get big size file and jpg file
        print root
        filter_list =  [ join(root,name) for name in files if getsize(join(root,name))>filter_size*1024*1024 or name[-3:] == 'jpg' ]
        print filter_list #old file path list
        new_filter_list = []
        for file in filter_list:
            split_file = file.split('\\')
            del(split_file[-2])
            split_file[-1] = split_file[-1].lower()
            newpath = ''
            for i in split_file:
                newpath = newpath + i + '\\'
            newpath = newpath[:-1] 
            new_filter_list.append(newpath)
        print new_filter_list
        for num,value in enumerate(filter_list):
            shutil.move(value,new_filter_list[num])

def rename(path):
    for root,dirs,files in os.walk(path):
        for file in files:
            print file


if __name__ == '__main__':
    # filesize = getdirsize(r'D:\git_hub')
    # print filesize
    path = u'F:\影视\电影'
    rename(path)