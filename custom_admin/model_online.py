#!/home/alonglry/.virtualenvs/django18/bin/python

################################################################################
#                                                                              #
# file name: /custome_admin/model_online.py                                    #
# description:                                                                 #
#                                                                              #
################################################################################
#                                                                              #
# version date       by              change                                    #
# 1.0     05/11/2016 awai            initial release                           #
# 1v1     11/02/2017 awai            add import os
#                                                                              #
################################################################################


import sys
import os
from file import getfile, writefile
from db import sqlexecute
from manage import manage

command = sys.argv[1]

tbl_list = ['id','status','project','model file name','table name','verbose name','verbose name plural','ordering','definition','unicode','model form','backup','retention d','remark']
col_list = ['id','project','table name','model file name','column name','sn','verbose name','verbose name plural','data type','min length','max length','decimal place','path','definition','default value','nullable','blank','unique key','choice options','model form','foreign key table','foreign key column','foreign key on delete','remark']
fun_list = ['id','project','model file name','table name','function']


##
## class: all_table_functions object
## parameter: all_table_functions data
## last update: 05/11/2016
## 
class Models_fn:
	def __init__(self,db,fun_list):
		try:
			self.script = '\t' + db[0][fun_list.index('function')].replace('\n','\n\t')
		except:
			self.script = ''

##
## class: django model file object
## parameter: all_tables data, all_tables field list
## last update: 05/11/2016
## 
class Models_f:
	
	def __init__(self,db,tbl_list):		
		self.project  = db[tbl_list.index('project')]
		self.file = db[tbl_list.index('model file name')]
		self.table = db[tbl_list.index('table name')]
		self.existing = getfile(self.project,self.file)
		self.script = self.existing
			
	def setImport(self):
		imp = ['import datetime',
		       'from django.db import models',
			   'from django.utils import timezone',
			   'from django.forms import ModelForm',
			   'from django.core.validators import MaxValueValidator, MinValueValidator',
			   'from django.db.models import F,Sum,Avg,Max,Min']
		for i in imp:		
			if self.script.find(i) == -1:
				self.script = self.script + i + '\n'
	
	def saveFile(self,script):
		try:
			o = self.existing.find('###begining of %s###\n' % self.table)
			p = self.existing.find('###end of %s###\n' % self.table)
			q = len('###end of %s###\n' % self.table)
			
			if o == -1:
				self.script = self.script + '\n\n' + script
			else:
				p1 = self.script[:o]
				p2 = self.script[p+q:]
				self.script = p1 + script + p2
				
			writefile(self.project,self.file,self.script)
		except:
			return 'fail'
		else:
			return 'success'
	
	def saveInit(self):
		tmp = getfile(self.project,'__init__.py')
		tmp2 = 'from ' + self.file.replace(' ','_')[:-3] + ' import *'
		
		o = tmp.find(tmp2)
		if o == -1:
			tmp = tmp.replace('# to be imported','# to be imported\n' + tmp2)
			writefile(self.project,'__init__.py',tmp)

####################################################################################################################
# name: models_c
# type: class
# import by: na
# use: main view module for accounts page
####################################################################################################################
# version author	description                      																												date
# 1.0     awai		initial release                  																												05/11/2016
# 1.1     awai		remove ,to_field='" + str(a[col_list.index('foreign key column')]) + " in foreignkey		18/10/2017
# 1.2			awai		fix m table foreignkey issue																														18/10/2017
####################################################################################################################
		
class Models_c:
	
	def __init__(self,db,col_list):
		
		self.script = ''
		#self.save   = ''
		self.form   = ''
		self.backup = ''
		
		for a in db:			
			
			#form
			if a[col_list.index('model form')] == 'Y':
				self.form = self.form + "'%s'," % a[col_list.index('column name')]
		
			#backup model columns
			
			if a[col_list.index('foreign key table')] <> '':
				self.name = a[col_list.index('column name')] + '_id'
				self.type = 'IntegerField'
			else:
				self.name = a[col_list.index('column name')]
				self.type = self.setType(a[col_list.index('data type')])
				
			tmp = '\t' + self.name + ' = models.' + self.type + '('
			
			if self.type == 'CharField':
				tmp = tmp + 'max_length=' + a[col_list.index('max length')] + ','
			elif self.type == 'IntegerField':
				tmp = tmp
			elif self.type == 'DecimalField':
				tmp = tmp + 'max_digits=%s,decimal_places=%s,' % (str(len(a[col_list.index('max length')])+int(a[col_list.index('decimal place')])),a[col_list.index('decimal place')])
			elif self.type == 'DateField' or self.type == 'DateTimeField':
				tmp = tmp
			
			tmp = tmp + 'null=True,blank=True)\n'
			self.backup = self.backup + tmp
			
			#model columns
			tmp = '\t' + a[col_list.index('column name')] + ' = models.'
			
			if a[col_list.index('foreign key table')] <> '':
				tmp = tmp + "ForeignKey('" + str(a[col_list.index('foreign key table')]) + "',on_delete=models." + str(a[col_list.index('foreign key on delete')]) + ','
				
				#if a[col_list.index('auto save foreign key')] == 'Y':
				#	self.save = self.save + '\t\t' + a[col_list.index('foreign key table')] + '.objects.get_or_create(' + a[col_list.index('foreign key column')] + '=self.' +a[col_list.index('foreign key column')]
				if a[col_list.index('nullable')] == 'Y':
					tmp = tmp + 'null=True,'
				if a[col_list.index('blank')] == 'Y':
					tmp = tmp + 'blank=True,'
				if a[col_list.index('unique key')] == 'Y':
					tmp = tmp + 'unique=True,'
				if a[col_list.index('verbose name')] <> '':
					tmp = tmp + "verbose_name='" + str(a[col_list.index('verbose name')]) + "',"						
			else:
				self.type = self.setType(a[col_list.index('data type')])
				self.validator = ''
				
				#data type
				tmp = tmp + self.type + '( '
				
				#verbose name
				if a[col_list.index('verbose name')] <> '':
					tmp = tmp + "'" + a[col_list.index('verbose name')] + "',"
					
				#min/max length
				if self.type == 'CharField':
					tmp = tmp + 'max_length=' + a[col_list.index('max length')] + ','
				elif self.type == 'IntegerField':
					if a[col_list.index('min length')] <> '':
						self.validator = self.validator + 'MinValueValidator(' + a[col_list.index('min length')] + '),'
					if a[col_list.index('max length')] <> '':
						self.validator = self.validator + 'MaxValueValidator(' + a[col_list.index('max length')] + '),'
					if self.validator <> '':
						tmp = tmp + 'validators=[' + self.validator[:-1] + '],'
				elif self.type == 'DecimalField':
					tmp = tmp + 'max_digits=%s,decimal_places=%s,' % (str(len(a[col_list.index('max length')])+int(a[col_list.index('decimal place')])),a[col_list.index('decimal place')])
				
				if (self.type == 'DateField' or self.type == 'DateTimeField') and a[col_list.index('default value')] == 'auto now':
					tmp = tmp + 'auto_now=True,'
				if self.type == 'Decimal