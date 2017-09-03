#!/home/alonglry/.virtualenvs/django18/bin/python

##########################################################
#                                                        #
# file name: /custome_admin/backup.py                    #
# description: backup and delete expired backups in      #
#              database                                  #
#                                                        #
##########################################################
#                                                        #
# version date       by              change              #
# 1.0     23/04/2016 Awai            initial release     #
# 1.1     02/02/2017 Awai            update log message  #
##########################################################

import sys
import datetime
from db import sqlexecute
from model import tbl_list, col_list

class obj_backup:
	
	def __init__(self,db):
		
		self.table = db[1]
		self.project = db[0]
		self.ret_d = db[2]
		self.db_table = self.project + "_" + self.table
		self.db_table_m = self.db_table + "_m"
		self.bk_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		
	def setColumn(self):
		
		sql = '''SELECT column_name,foreign_key_table FROM all_table_columns
			 WHERE project = "''' + self.project + '''" 
			 AND table_name = "''' + self.table + '";'
	
		tmp = sqlexecute(sql)
		
		result = ''
		
		for t in tmp:
			if t[1] == '':
				result = result + t[0] + ','
			else:
				result = result + t[0] + '_id,'
			
		self.column = result[:-1]
		
	def setRetention(self):
	
		if self.bk_date is not None:
			delta = datetime.timedelta(days=1)
			tmp = '('
			
			for i in range(0,self.ret_d):
				tmp = tmp + '"' + (datetime.datetime.now() - delta - delta * i).strftime("%Y-%m-%d") + '",'
				
			self.retention = tmp[:-1] + ')'
		
	
def get_table():
	
	sql = '''SELECT project,table_name,retention_d FROM all_tables 
			 WHERE backup = "Y"
			 AND project IS NOT NULL
			 AND table_name IS NOT NULL;'''
			 
	result = sqlexecute(sql)
	return result
	
def get_column(project,table):
	
	sql = '''SELECT column_name FROM all_table_columns
			 WHERE project = "''' + project + '''" 
			 AND table_name = "''' + table + '";'
	
	tmp = sqlexecute(sql)
	
	result = ''
	
	for t in tmp:
		result = result + t[0] + ','
		
	return result[:-1]

def sqlerror(err):
	result = 'SQL: ' + str(err[1]) + ' is having error. \nMessage: ' + str(err[0])
	
def backup():
	table = get_table()
	count = 0
	
	for t in table:
		obj_t = obj_backup(t)
		obj_t.setColumn()
		obj_t.setRetention()
		
		#remove existing backup for the day
		sql = 'DELETE FROM ' + obj_t.db_table_m + ' WHERE bk_date = "' + obj_t.bk_date + '";'
		
		try:
			sqlexecute(sql)
		except ValueError, e:
			print sqlerror(e)
		
		#backup for the day		
		sql = 'INSERT INTO ' + obj_t.db_table_m + '(bk_date,' + obj_t.column + ''') 
			   SELECT "''' + obj_t.bk_date + '",' + obj_t.column + ' FROM ' + obj_t.db_table + ';'
			   
		try:
			sqlexecute(sql)
			count = count + 1
			print obj_t.db_table + ' has been saved into ' + obj_t.db_table_m + ' for ' + obj_t.bk_date + '.'
		except ValueError, e:
			print obj_t.db_table + ' backup failed for ' + obj_t.bk_date + '.'
			print sql
			#print obj_t.db_table + ' backup failed. Error message: ' + sqlerror(e)
			
		#remove expired backups
		sql = 'DELETE FROM ' + obj_t.db_table_m + ' WHERE bk_date NOT IN ' + obj_t.retention + ';'
		
		try:
			sqlexecute(sql)
			print obj_t.db_table_m + ' cleanup done.'
		except ValueError, e:
			print obj_t.db_table + ' cleanup failed. Error message: ' + sqlerror(e)
		
		print '\n'
		
backup()