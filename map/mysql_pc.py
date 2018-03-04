#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-14 22:48:24
# @Author  : robin (robin.zhu@nokia.com)


import MySQLdb,sys
from _mysql_exceptions import (
    Warning, Error, InterfaceError, DataError,
    DatabaseError, OperationalError, IntegrityError, InternalError,
    NotSupportedError, ProgrammingError)


class MYSQL_OP():
	def __init__(self,host_name,user_name,password,database):
		self.db = MySQLdb.connect(host=host_name,user=user_name,passwd=password,db=database) 

	def __enter__(self):
		return self.db

	def __exit__(self,type,value,traceback):
		print "close mysql connection"
		self.db.close()

class MYSQL_PC():
	def __init__(self,db): 
		self.cursor = db.cursor()
		self.db = db
		self.table_args = {}

	def _excute_fetch(self,sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def show_tables(self,table_name):
		return self._excute_fetch("select * from {0}".format(table_name))

	def get_data_by(self,table_name,name):
		return self._excute_fetch("select * from {0} where LAST_NAME='{1}'".format(table_name,name))

	def get_table_fields(self,table_name):
		try:
			return map( lambda x:x[0] , self._excute_fetch("desc {}".format(table_name)) )
		except ProgrammingError as e:
			print  e[1]
			return []
		

	def insert_data(self,table_name,dictory):
		if not self.table_args.has_key(table_name):
			print "generate {} args".format(table_name)
			self.table_args[table_name] = self.get_table_fields(table_name)
		values = tuple(dictory[key] if dictory.has_key(key) else " " for key in self.table_args[table_name])
		sql = """ insert into {0} ({1})
		values {2}""".format(table_name,",".join(self.table_args[table_name]),values)
		print  sql
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except Exception as e:
			print e
			self.db.rollback()


	def create_table(self,table_name,char_len=255):
		args = table_args[table_name]
		tmp_sql = ["{0} char({1})".format(i,char_len) for i in args.split(",") ]
		sql = "CREATE TABLE {} ( ".format(table_name)
		for i in tmp_sql:
			sql = sql + i + " ,"
		sql = sql[:-1] + ")"
		print sql
		# self.cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
		# self.cursor.execute(sql)

	def create_text_table(self,table_name):
		args = table_args[table_name]
		tmp_sql = ["{0} text ".format(i) for i in args.split(",") ]
		sql = "CREATE TABLE {} ( ".format(table_name)
		for i in tmp_sql:
			sql = sql + i + " ,"
		sql = sql[:-1] + ")"
		print sql
		self.cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
		self.cursor.execute(sql)


def main():
	with MYSQL_OP("localhost","root","hello121","haha") as db:
		pc = MYSQL_PC(db)
		print  pc.show_tables("map_node")
		# dict2 = {"FIRST_NAME":"robin","LAST_NAME":"hua","AGE":30,"SEX":"M","INCOME":3000}
		# dict3 = {"JOB_NAME":"zezeze","DOWN_STREAM_NAME":"biebiebie","BUILD_NUMBER":"12"}
		# pc.create_table("map_node")
		# pc.create_text_table("map_node")
		# print pc.insert_data("map_node",dict1)
		# print type(tables),dir(tables),tables.__long__
		aa = pc.get_table_fields("map_node")
		print aa                        
		
if __name__ == '__main__':
	# dict1 = {'downstreamProjects': [u'DSP_Build_Store_Libraries_FBLRC1606'], 'subBuilds': ['DSP_UnitTest_CCSRT_Valgrind_FBLRC1606', 'DSP_Build_Kep_LRC_FBLRC1606,DSP_UnitTest_RT_FBLRC1606,DSP_Build_RT_FBLRC1606'], 'upstreamProjects': [], 'scm': ['https://svne1.access.nsn.com/isource/svnroot/BTS_SC_DSPHWAPI/FBLRC1606/trunk'], 'jobName': u'DSP_Build_Promo_FBLRC1606'}
	# for k,v in dict1.items():
	# 	dict1[k] = str(v)
	# 	# dict1[k] = ",".join(v)
	# print dict1
	# table_args = {"employee":"FIRST_NAME,LAST_NAME,AGE,SEX,INCOME","map_node":"jobName,downstreamProjects,subBuilds,upstreamProjects,scm"}
	main()
