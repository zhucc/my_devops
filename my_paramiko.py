#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-30 10:54:01
# @Author  : robin (robin.zhu@nokia.com)
# @Link    : http://example.org
# @Version : $Id$

import  paramiko as PK
ssh = PK.SSHClient()
ssh.set_missing_host_key_policy(PK.AutoAddPolicy())
ssh.connect("hzling101",22,"ca_hzpsscm","hello121")
stdin,stdout,stderror = ssh.exec_command("df -h")
print stdout.readlines()
ssh.close()