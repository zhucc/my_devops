#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-06 14:07:18
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    : 

from celery import Celery
app = Celery("demo")
app.config_from_object('celerytt.celeryconfig')