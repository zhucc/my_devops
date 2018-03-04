#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-06 11:25:49
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    : 

from datetime import timedelta
from celery.schedules import crontab

# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# Timezone
CELERY_TIMEZONE='Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'

# import
CELERY_IMPORTS = (
    'celerytt.task'
)

# schedules
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
         'task': 'celerytt.task.sendmail',
         'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
         'args': ("robin.zhu", )                           # 任务函数参数
    },
}