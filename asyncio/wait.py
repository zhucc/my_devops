#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-12 15:14:30
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    : 
from time import time

events_l = []
class Event(object):
    def __init__(self,*args,**kwagrs):
        self.callback = lambda : None
        events_l.append(self)

    def set_callback(self,callback):
        # print callback
        self.callback = callback

    def is_ready(self):
        result = self._is_ready()
        if result:
            # print self.callback.__closure__
            self.callback()
        return result

class SleepEvent(Event):

    def __init__(self,timeout):
        super(SleepEvent,self).__init__(timeout)
        self.timeout = timeout
        self.start_time = time()

    def _is_ready(self):
        return time() - self.start_time >= self.timeout

def run(tasks):
    for task in tasks:
        _next(task)
        print events_l
    while len(events_l):
        for event in events_l:
            # print "checking {}".format(event)
            if event.is_ready():
                print events_l
                events_l.remove(event)
                print events_l
                break

def _next(task):
    try:
        time_event =next(task)
        time_event.set_callback(lambda : _next(task))
    except StopIteration as e:
        print "stoping..."

def task(name):
    print (name,1)
    yield SleepEvent(1)
    print  (name,2)
    yield SleepEvent(3)
    print (name,3)


def upper_attr(future_class_name, future_class_parents, future_class_attr):
    '''返回一个类对象，将属性都转为大写形式'''
    #  选择所有不以'__'开头的属性
    print "calling upper_attr"
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
    # 将它们转为大写形式
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    
    print uppercase_attr
    # 通过'type'来做类对象的创建
    return type(future_class_name, future_class_parents, uppercase_attr)

  #  这会作用到这个模块中的所有类

__metaclass__ = upper_attr
class Foo(object):

    # 我们也可以只在这里定义__metaclass__，这样就只会作用于这个类中
    bar = 'bip'
    aa = "lala"

class Foo2(object):

    # 我们也可以只在这里定义__metaclass__，这样就只会作用于这个类中
    bar = 'bip'
    aa = "lala"
if __name__ == '__main__':
    import time
    run((task("robin"),task("mandy")))
