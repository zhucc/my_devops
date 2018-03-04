#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 13:44:35
# @Author  : robin (robin.zhu@nokia.com)
# @Description : 

from optparse import OptionParser

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="filename",
                      help="read data from FILENAME")
    parser.add_option("-v", "--verbose",
                      action="store", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    if options.verbose:
        print "reading %s..." % options.filename

if __name__ == "__main__":
    main()


