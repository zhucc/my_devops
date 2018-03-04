#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-06 11:33:27
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    : 

# tasks.py
import time
from celerytt import app


@app.task
def sendmail(mail):
    print('sending mail to %s...' % mail[0])
    time.sleep(10.0)
    print('mail sent.')