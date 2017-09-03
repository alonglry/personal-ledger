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

##
## class: all_table_columns object
## parameter: all_table_columns data, table name, all_table_columns field list
## last update: 05/11/2016
## 	
		
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
			self.type = self.setType(a[col_list.index('data type')])
			
			if a[col_list.index('foreign key table')] <> '':
				self.name = a[col_list.index('column name')] + '_id'
			else:
				self.name = a[col_list.index('column name')]
				
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
				tmp = tmp + "ForeignKey('" + str(a[col_list.index('foreign key table')]) + "',to_field='" + str(a[col_list.index('foreign key column')]) + "',on_delete=models." + str(a[col_list.index('foreign key on delete')]) + ','
				
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
				if self.type == 'DecimalField' and a[col_list.index('default value')] <> '':
					tmp = tmp + 'default=%s,' % a[col_list.index('default value')]
				if self.type == 'ImageField':
					tmp = tmp + self.setPicpath(a[col_list.index('project')],a[col_list.index('path')])
				if self.type <> 'DateField' and self.type <> 'DateTimeField' and self.type <> 'DecimalField' and a[col_list.index('default value')] <> '':
					tmp = tmp + 'default="' + a[col_list.index('default value')] + '",'
				if a[col_list.index('nullable')] == 'Y':
					tmp = tmp + 'null=True,'
				if a[col_list.index('blank')] == 'Y':
					tmp = tmp + 'blank=True,'
				if a[col_list.index('unique key')] == 'Y':
					tmp = tmp + 'unique=True,'
				if a[col_list.index('choice options')] <> '':
					tmp = tmp + 'choices=' + self.setChoice(a[col_list.index('choice options')]) + ','
					
			tmp = tmp[:-1] + ')'
				
			self.script = self.script + '\n' + tmp
				
		self.script = self.script.replace('( ','(')
		self.form   = self.form[:-1]
		self.backup = self.backup + '\tbk_date = models.DateField()\n'
				
		#if self.save <> '':
		#	self.script = self.script + '\n\n\tdef save(self, *args, **kwargs):\n' + self.save + '\t\tsuper(' + name + ', self).save(*args, **kwargs)'
		
	def setType(self,t):
		tmp = ''
		if t == 'varchar':
			tmp = 'CharField'
		elif t == 'float':
			tmp = 'DecimalField'
		elif (t == 'int' or t == 'integer'):
			tmp = 'IntegerField'
		elif (t == 'datetime'):
			tmp = 'DateTimeField'
		elif t == 'date':
			tmp = 'DateField'
		elif t == 'url':
			tmp = 'URLField'
		elif t == 'image':
			tmp = 'ImageField'
		return tmp
		
	def setChoice(self,choice):
		tmp = ''
		for a in choice.split(','): 
			tmp = tmp + "('" + a.strip() + "','" + a.strip() + "'),"
		tmp = '(' + tmp[:-1] + ')'
		return tmp
	
	def setPicpath(self,project,path):
		p = 'personal_finance/static/' + project + '/' + path
		import os
		if os.path.exists(p):
			tmp = ''
		else:
			os.makedirs(p)
		
		return "upload_to='"  + project + '/' + path + "',default='" + project + "/image/no-image.jpg',"
		
##
## class: all_tables object
## parameter: all_tables data, all_tables field list
## last update: 05/11/2016
## 
class Models_t:
	
	def __init__(self, db, tbl_list):
		
		self.project    = db[tbl_list.index('project')]
		self.file       = db[tbl_list.index('model file name')]
		self.init       = 'from ' + db[tbl_list.index('model file name')].replace(' ','_') + ' import *'
		self.table      = db[tbl_list.index('table name')]
		self.verbose    = db[tbl_list.index('verbose name')]
		self.verbosep   = db[tbl_list.index('verbose name plural')]
		self.ordering   = db[tbl_list.index('ordering')]
		self.definition = db[tbl_list.index('definition')]
		#self.unicode    = str(db[tbl_list.index('unicode')])
		self.form       = db[tbl_list.index('model form')]
		self.backup     = db[tbl_list.index('backup')]
		
		self.p1 = '###begining of %s###\n' % self.table
		self.p2 = 'class %s(models.Model):\n' % self.table
		
		#model meta class
		self.meta = self.setMeta()
		#model form class
		self.form = self.setForm()
		#model backup class
		self.backup = self.setBackup()
		#unicode method
		#self.unicode = self.setUnicode()
		
		self.p4 = '###columns of %s###' % self.table
		self.p6 = '###end of %s###\n' % self.table
		
		#final script for the model
		self.script = self.setScript()
		
	def setForm(self):
		tmp = ''
		self.p7 = '###form columns of %s###' % self.table
		
		if self.form == 'Y':
			#tmp = tmp + '###begining of %s_form###\n' % self.table
			tmp = tmp + 'class %s_form(ModelForm):\n\tclass Meta:\n\t\tmodel = %s\n\t\tfields = [%s]\n' % (self.table,self.table,self.p7)
			#tmp = tmp + '###end of %s_form###\n' % self.table
		
		return tmp
		
	def setBackup(self):
		tmp = ''
		self.p8 = '###backup columns of %s_m###' %self.table
		
		if self.backup == 'Y':
			#tmp = tmp + '###begining of %s_m###\n' % self.table
			tmp = tmp + 'class %s_m(models.Model):\n%s' % (self.table, self.p8)
			#tmp = tmp + '###end of %s_m###\n' % self.table
			
		return tmp
			
	def setMeta(self):
		tmp = ''
		
		if self.verbose is not None and self.verbose <> ''  : tmp = tmp + "\t\tverbose_name = '%s'\n" % self.verbose
		if self.verbosep is not None and self.verbosep <> '': tmp = tmp + "\t\tverbose_name_plural = '%s'\n" % self.verbosep 
		if self.ordering is not None and self.ordering <> '': tmp = tmp + "\t\tordering = [%s]\n" % listsplit(self.ordering)
		
		if tmp <> '':
			tmp = '\tclass Meta:\n' + tmp
		
		return tmp
	
	#def setUnicode(self):
	#	tmp = ''		
	#	if self.unicode <> '': tmp = '\tdef __unicode__(self):\n\t\treturn ' + self.unicode + '\n'		
	#	return tmp
				
	def setScript(self):
		tmp = ''
		tmp = self.p2		
		if self.meta <> '':    tmp = tmp + '\n' + self.meta
		tmp = tmp + self.p4
		#if self.unicode <> '': tmp = tmp + '\n\n' + self.unicode
		tmp = tmp + '\n'
		return tmp
		
##
## function: validate django model date
## parameter: project name, file name, table name
## last update: 21/05/2017
## 

def check_model(p,f,t):

	tbl = tbl_list[2:]
	col = col_list[1:]
	fun = fun_list[1:]
	
	error = ''

	#get functions
	sql = "SELECT %s FROM ledger_all_table_functions WHERE project = '%s' AND model_file_name = '%s' AND table_name = '%s';" % (listsplit2(fun),p,f,t)
	fn = sqlexecute(sql)
	
	try:
		p = str(fn[0]).find('    ')
		if p <> -1:
			error = error + '\nfunction indend error\n"' + str(fn[0])[max(p-20,0):p+24] + '"'
	except:
		error = error
	
	return error

##
## function: prepare django model file
## parameter: project name, file name, table name
## last update: 11/09/2016
## 
def write_model_file(p,f,t):

	tbl = tbl_list[2:]
	col = col_list[1:]
	fun = fun_list[1:]
		
	#get tables
	sql = "SELECT %s FROM ledger_all_tables WHERE project = '%s' AND model_file_name = '%s' AND table_name = '%s';" % (listsplit2(tbl),p,f,t)
	m = sqlexecute(sql)[0]
	obj_t = Models_t(m,tbl)
	
	#get file
	obj_f = Models_f(m,tbl)
	
	#get columns
	sql = "SELECT %s FROM ledger_all_table_columns WHERE project = '%s' AND model_file_name = '%s' AND table_name = '%s' ORDER BY sn;" % (listsplit2(col),p,f,t)
	obj_c = Models_c(sqlexecute(sql),col)
	
	#get functions
	sql = "SELECT %s FROM ledger_all_table_functions WHERE project = '%s' AND model_file_name = '%s' AND table_name = '%s';" % (listsplit2(fun),p,f,t)
	obj_fn = Models_fn(sqlexecute(sql),fun)
	
	#get script
	model  = obj_t.script.replace(obj_t.p4,obj_c.script + '\n\n' + obj_fn.script)
	
	if obj_c.form <> '':
		form = obj_t.form.replace(obj_t.p7,obj_c.form)
	else:
		form = ''
		
	backup = obj_t.backup.replace(obj_t.p8,obj_c.backup)
		
	script = '###begining of %s###\n\n' %t + model + '\n' + form + '\n' + backup + '\n###end of %s###\n' %t
	
	#save script
	obj_f.saveInit()
	obj_f.setImport()
	
	return obj_f.saveFile(script)
		
def listsplit(a):
	tmp = ''
	
	if type(a) is str:
		for l in a.split(','):
			tmp = tmp + "'" + str(l) + "',"
	elif type(a) is list:
		for l in a:
			tmp = tmp + "'" + str(l) + "',"
	elif type(a) is tuple:
		for l in a:
			tmp = tmp + "'" + str(l) + "',"
	tmp = tmp.replace(' ','_')
	return tmp[:-1]

def listsplit2(a):
	tmp = listsplit(a)
	tmp = tmp.replace("'",'')
	return tmp

if command == 'preparemigration':
	#project name
	p = sys.argv[2]
	
	#file name
	f = sys.argv[3]
		
	#table name
	t = sys.argv[4]
	
	error = check_model(p,f,t)
	
	if error == '':
		print(write_model_file(p,f,t))
	else:
		print error
	
elif command == 'makemigration':
	p = sys.argv[2]
	manage('makemigrations',p)