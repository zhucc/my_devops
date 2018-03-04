#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-31 15:43:56
# @Author  : robin (robin.zhu@nokia.com)
# @Link    : http://example.org
# @Version : $Id$


class MAPNODE(dict):
    part = "HWAPI"
    host = "1.1.1.1"
    def __init__(self,args):
        self.__dict__.update(args)
        self.__dict__.setdefault("part",self.part)
        self.__dict__.setdefault("host",self.host)
        # self.__dict__["host"] = "127.0.0.1" if not self.__dict__.has_key("host") else ""

    def __getitem__(self, k):
        return self.__dict__.get(k, None)
         
    def __setitem__(self, k, value):
        self.__dict__[k] = value

    def __delitem__(self , k):
    	del self.__dict__[k]

    def __repr__(self):
        return "type:{0} value:{1}".format(type(self),self.__dict__)


if __name__ == '__main__':

    s = MAPNODE({"name":"lalalala","downstream":"hehehehe"})
    del s.name
    print s
    s = MAPNODE({"name":"lalalala","downstream":"hehehehe"})
    print s
    MAPNODE.host = "127.1.1.1"
    b = MAPNODE({"name":"hehehe","downstream":"pupupu"})
    print b,s
    MAPNODE.part = "CCS"
    l = MAPNODE({"name":"pupupu","downstream":"huahuhauuhua"})
    print l