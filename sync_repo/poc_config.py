#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-01 16:15:30
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    :

import os
from os import path as osp
# gerrit user name where public key of jenkins account add to .
# use to commit gerrit changes
gerrit_host = "*****"
gerrit_user = "********"
gerrit_token = "********"
gerrit_branch = "master"
components = "recipes-components"
workspace = os.getenv("WORKSPACE", osp.expanduser('~'))