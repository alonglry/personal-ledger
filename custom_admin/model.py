#!/home/alonglry/.virtualenvs/django18/bin/python

################################################################################
#                                                                              #
# file name: /custome_admin/model.py                                           #
# description:                                                                 #
#                                                                              #
################################################################################
#                                                                              #
# version date       by              change                                    #
# 1.0     19/04/2016 Awai            initial release                           #
# 1.1     01/05/2016 Awai            add model_form logic                      #
# 1.2     04/05/2016 Awai            fix bug in adding rows from stg to base   #
# 1.3     21/05/2016 Awai            add ImageField and URLField support       #
# 1.4     15/06/2016 Awai            add validation function                   #
# 1.5     25/06/2016 Awai            add validation function checking if table #
#									 has no columns                            #
# 1.6     16/07/2016 Awai            update model import to include F,Sum,Avg, #
#                                    Max,Min                                   #
# 1.7     16/07/2016 Awai            add default value for DecimalField        #
# 1.8     17/07/2016 Awai            add validation for decimal field          #
# 1.9     25/07/2016 Awai            add buildmodel for consolidated commands  #
# 1.9     01/09/2016 Awai            change base table                         #
# 2.0     02/09/2016 Awai            add DateTimeField                         #
# 2.1     11/09/2016 Awai            insert customised function from database  #
#                                                                              #
################################################################################

import csv
import datetime
import sys
import os
import urllib2

from file import getfile, writefile
from db import sqlexecute
from manage import manage
	
try:
	command = sys.argv[1]
except IndexError:
	command = ''
	
tbl_list = ['id','status','project','model file name','table name','verbose name','verbose name plural','ordering','definition','unicode','model form','backup','retention d','remark']

col_list = ['id','project','table name','model file name','column name','verbose name','verbose name plural','data type','min length','max length','decimal place','path','definition','default value','nullable','blank','unique key','choice options','model form','foreign key table','foreign key column','foreign key on delete','auto save foreign key','remark']

trim_list = []

cap_list = ['foreign key on delete','auto save foreign key','nullable','blank','unique key','model form','backup']
	
def red(self):
	return '\033[91m' + str(self) + '\033[0m'

def yellow(self):
	return '\033[93m' + str(self) + '\033[0m'

def bold(self):
	return '\033[1m' + str(self) + '\033[0m'

##
## class: all_table_functions object
## parameter: all_table_functions data
## last update: 05/11/2016
## 
class Models_fn:
	def __init__(self,db):
		self.script = ''
		
		for a in db:
			tmp = ''
			tmp = tmp + '\t' + a[4].replace('\n','\n\t')
			self.script = self.script + tmp + '\n'
			
		self.script = '\n' + self.script

##
## class: django model file object
## parameter: all_tables data, all_tables field list
## last update: 05/11/2016
## 
class Models_f:
	
	def __init__(self,db,tbl_list):
		self.imp = 'import datetime\nfrom django.db import models\nfrom django.utils import timezone\nfrom django.forms import ModelForm\nfrom django.core.validators import MaxValueValidator, MinValueValidator\nfrom django.db.models import F,Sum,Avg,Max,Min\n\n'
		
		self.project  = db[tbl_list.index('project')]
		self.filename = db[tbl_list.index('model file name')]
		self.existing = getfile(self.project,self.filename)
		
		self.script = self.imp
		
	def setModel(self,new):
		tmp = new
		
		o = self.existing.find('###end of %s customised###\n' % self.table)
		p = self.existing.find('###end of %s###\n' % self.table)
		if o == -1:
			tmp = tmp + '###end of %s customised###\n' % self.table
		else:
			tmp2 = self.existing[(p + len('###end of %s###\n' % self.table)):(o + len('###end of %s customised###\n' % self.table))]
			if tmp2 <> '###end of %s customised###\n' % self.table:
				tmp = tmp + tmp2
			else:
				tmp = tmp + '###end of %s customised###\n' % self.table
			
		self.script = self.script + tmp + '\n'
	
	def setBackup(self,new):
		if new <> '':
			tmp = new
			
			o = self.existing.find('###end of %s_m customised###\n' % self.table)
			p = self.existing.find('###end of %s_m###\n' % self.table)
			
			if o == -1:
				tmp = tmp + '###end of %s_form customised###\n' % self.table
			else:
				tmp2 = self.existing[(p + len('###end of %s_m###\n' % self.table)):(o + len('###end of %s_m customised###\n' % self.table))]
				if tmp2  <> '###end of %s_m customised###\n' % self.table:
					tmp = tmp + '\t' + tmp2
				else:
					tmp = tmp + '###end of %s_m customised###\n' % self.table 
			self.script = self.script + tmp + '\n'
	
	def setTable(self,table):
		self.table = table
	
	def setForm(self,new,):
		if new <> '':
			tmp = new
			
			o = self.existing.find('###end of %s_form customised###\n' % self.table)
			p = self.existing.find('###end of %s_form###\n' % self.table)
			
			if o == -1:
				tmp = tmp + '###end of %s_form customised###\n' % self.table
			else:
				tmp2 = self.existing[(p + len('###end of %s_form###\n' % self.table)):(o + len('###end of %s_form customised###\n' % self.table))]
				if tmp2  <> '###end of %s_form customised###\n' % self.table:
					tmp = tmp + tmp2
				else:
					tmp = tmp + '###end of %s_form customised###\n' % self.table
				 
			self.script = self.script + tmp + '\n'
	
	def saveFile(self):
		writefile(self.project,self.filename,self.script)
	
	def saveInit(self):
		tmp = getfile(self.project,'__init__.py')
		tmp2 = 'from ' + self.filename.replace(' ','_')[:-3] + ' import *'
		
		o = tmp.find(tmp2)
		if o == -1:
			tmp = tmp.replace('# to be imported','# to be imported\n' + tmp2)
			writefile(self.project,'__init__.py',tmp)
			
	def clearInit(self):
		tmp = getfile(self.project,'__init__.py')
		
		o = tmp.find('# to be imported')
		p = tmp.find('# end of import')
		
		tmp = tmp[:o] + '# to be imported\n'+ tmp[p:]
		
		writefile(self.project,'__init__.py',tmp)

##
## class: all_table_columns object
## parameter: all_table_columns data, table name, all_table_columns field list
## last update: 05/11/2016
## 	
class Models_c:
	
	def __init__(self,db,name,col_list):
		
		self.script = ''
		self.save   = ''
		self.form   = ''
		self.backup = ''
		
		for a in db:
			if a[col_list.index('table name')] == name:
			
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
				
		if self.save <> '':
			self.script = self.script + '\n\n\tdef save(self, *args, **kwargs):\n' + self.save + '\t\tsuper(' + name + ', self).save(*args, **kwargs)'
		
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
		p = '../static/' + project + '/' + path
		if not os.path.exists(p):
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
		self.unicode    = str(db[tbl_list.index('unicode')])
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
		self.unicode = self.setUnicode()
		
		self.p4 = '###columns of %s###' % self.table
		self.p6 = '###end of %s###\n' % self.table
		
		#final script for the model
		self.script = self.setScript()
		
	def setForm(self):
		tmp = ''
		self.p7 = '###form columns of %s###' % self.table
		
		if self.form == 'Y':
			tmp = tmp + '###begining of %s_form###\n' % self.table
			tmp = tmp + 'class %s_form(ModelForm):\n\tclass Meta:\n\t\tmodel = %s\n\t\tfields = [%s]\n' % (self.table,self.table,self.p7)
			tmp = tmp + '###end of %s_form###\n' % self.table
		
		return tmp
		
	def setBackup(self):
		tmp = ''
		self.p8 = '###backup columns of %s_m###' %self.table
		
		if self.backup == 'Y':
			tmp = tmp + '###begining of %s_m###\n' % self.table
			tmp = tmp + 'class %s_m(models.Model):\n%s' % (self.table, self.p8)
			tmp = tmp + '###end of %s_m###\n' % self.table
			
		return tmp
			
	def setMeta(self):
		tmp = ''
		
		if self.verbose is not None and self.verbose <> ''  : tmp = tmp + "\t\tverbose_name = '%s'\n" % self.verbose
		if self.verbosep is not None and self.verbosep <> '': tmp = tmp + "\t\tverbose_name_plural = '%s'\n" % self.verbosep 
		if self.ordering is not None and self.ordering <> '': tmp = tmp + "\t\tordering = [%s]\n" % listsplit(self.ordering)
		
		if tmp <> '':
			tmp = '\tclass Meta:\n' + tmp
		
		return tmp
	
	def setUnicode(self):
		tmp = ''
		
		if self.unicode <> '': tmp = '\tdef __unicode__(self):\n\t\treturn ' + self.unicode + '\n'
		
		return tmp
				
	def setScript(self):
		tmp = ''
		tmp = self.p1 + self.p2		
		if self.meta <> '':    tmp = tmp + '\n' + self.meta
		tmp = tmp + self.p4
		if self.unicode <> '': tmp = tmp + '\n\n' + self.unicode
		tmp = tmp + '\n' + self.p6
		return tmp

def load_stg_table(tbl,loc,cols):

	try:		
		with open('%s/%s.csv' % (loc,tbl), 'rb') as csvfile:
			day = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			count = 0
			
			#read csv file
			print 'read from ' + red(tbl + '.csv') + '...'
			line = csv.DictReader(csvfile, delimiter=',')
			
			#truncate staging table
			print 'remove existing records in %s...' % red(tbl)
			sql = 'TRUNCATE TABLE %s;' % tbl
			sqlexecute(sql)
			
			#insert into staging table
			print 'insert new records into %s...' % red(tbl)
			for row in line:
				a,b = ['','']
				for col in cols:
					b = b + '"' + row[col] + '",'
					a = a + col.replace(' ','_') + ","
				a = a + "last_update_date"
				b = b + '"' + day + '"'				
				
				sql = "INSERT INTO %s (%s) VALUES(%s);""" % (tbl,a,b)
				
				try:
					sqlexecute(sql)
					count = count + 1
				except ValueError, e:
					sqlerror(e)
				
			print 'inserted %s rows into %s' % (bold(count),red(tbl))
			
			#rename loaded csv file
			os.rename('%s/%s.csv' % (loc,tbl), '%s/%s_%s.csv' % (loc,tbl,day))
			
	except IOError:
		print '%s not exists' % red(tbl + '.csv')
		
	print '\n'
	
	return

def load_stg_table_online(tbl,cols):

	try:
		if tbl == 'stg_all_tables': url = 'https://docs.google.com/spreadsheets/d/1gOiYEl6bsx40Ht2hzul40YeSdy1TKW1EVxnotirvcbc/pub?gid=983104586&single=true&output=csv'
		elif tbl == 'stg_all_table_columns': url = 'https://docs.google.com/spreadsheets/d/1gOiYEl6bsx40Ht2hzul40YeSdy1TKW1EVxnotirvcbc/pub?gid=0&single=true&output=csv'
		
		csvfile = urllib2.urlopen(url)
		
		day = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		count = 0
		
		#read csv file
		print 'read from ' + red(tbl + '.csv') + '...'
		line = csv.DictReader(csvfile, delimiter=',')
		
		#truncate staging table
		print 'remove existing records in %s...' % red(tbl)
		sql = 'TRUNCATE TABLE %s;' % tbl
		sqlexecute(sql)
		
		#insert into staging table
		print 'insert new records into %s...' % red(tbl)
		for row in line:
			a,b = ['','']
			for col in cols:
				b = b + '"' + row[col] + '",'
				a = a + col.replace(' ','_') + ","
			a = a + "last_update_date"
			b = b + '"' + day + '"'				
			
			sql = "INSERT INTO %s (%s) VALUES(%s);""" % (tbl,a,b)
			
			try:
				sqlexecute(sql)
				count = count + 1
			except ValueError, e:
				sqlerror(e)
			
		print 'inserted %s rows into %s' % (bold(count),red(tbl))
			
	except IOError:
		print '%s not exists' % red(tbl + '.csv')
		
	print '\n'
	
	return

def load_model_table(tbl,filter,cols):

	ids          = ''
	ids_1062     = '' #duplicate row
	add_count    = 0	
	delete_count = 0
	modify_count = 0
	day          = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	
	#get staging table
	print 'read from %s...'	% red('stg_' + tbl)
	
	a = listsplit2(cols)
	
	sql = 'SELECT id, action, status, %s from %s WHERE (status = "" or status IS NULL) AND action <> "";' % (a,'stg_' + tbl)
	
	if filter <> 'all' and filter.find('%') == -1:
		sql = sql[:-1] + ' AND table_name in (%s);' % listsplit(filter)
	elif filter <> 'all' and filter.find('%') <> -1:
		sql = sql[:-1] + ' AND table_name like (%s);' % listsplit(filter)
		
	sql = sql[:-1] + ' ORDER BY action DESC;'
	
	stg = sqlexecute(sql)
	
	#insert
	if len(stg) == 0:
		print 'no new rows to be updated into %s' % red(tbl)
	else:
		print 'insert into %s...' % red(tbl)
		for row in stg:
			if row[1] == 'add':
				
				sql = "INSERT INTO %s (%s, last_update_date) VALUES (%s,'%s');" % ('ledger_'+tbl,a,listsplit3(row[3:],cols),day)
				
				try:
					sqlexecute(sql)
					ids = ids + str(row[0]) + ','
					add_count = add_count + 1
				except ValueError, e:
					if sqlerror(e) == '1062':
						ids_1062 = ids_1062 + str(row[0]) + ','
					
			elif row[1] == 'delete':
				sql = 'DELETE FROM %s WHERE project="%s" AND table_name="%s";' % ('ledger_'+tbl,row[cols.index('project')+3],row[cols.index('table name')+3])
				
				if 'column name' in cols:
					sql = sql[:-1] + ' AND column_name="%s";' % row[cols.index('column name')+3]
				
				try:
					sqlexecute(sql)				
					ids = ids + str(row[0]) + ','
					delete_count = delete_count + 1
				except ValueError, e:
					sqlerror(e)
					
			elif row[1] == 'modify':
				sql = 'UPDATE %s SET %s, last_update_date = "%s" WHERE project="%s" AND table_name="%s";' % ('ledger_'+tbl,listsplit4(row,cols),day,row[cols.index('project')+3],row[cols.index('table name')+3])
				
				if 'column name' in cols:
					sql = sql[:-1] + ' AND column_name="%s";' % row[cols.index('column name')+3]
				
				try:
					sqlexecute(sql)				
					ids = ids + str(row[0]) + ','
					modify_count = modify_count + 1
				except ValueError, e:
					sqlerror(e)
				
		#update staging table status
		sql = 'UPDATE stg_%s SET status = "DONE" WHERE id in (%s);' % (tbl,listsplit(ids))
		sqlexecute(sql)
		
		sql = 'UPDATE stg_%s SET status = "DUPLICATE" WHERE id in (%s);' % (tbl,listsplit(ids_1062))
		sqlexecute(sql)
		
		print 'added %s rows' % bold(str(add_count))
		print 'deleted %s rows' % bold(str(delete_count))
		print 'modified %s rows' % bold(str(modify_count))
	
	print '\n'
	
	return
	
def validate_model_table(file):
	ind = False
	
	#validate if all tables have columns
	sql = 'SELECT distinct project,model_file_name,table_name FROM ledger_all_tables;'
	
	stg = sqlexecute(sql)
	
	if file <> 'all' and file.find('%') == -1:
		sql = sql[:-1] + ' AND model_file_name in (%s);' % listsplit(file)
	elif file <> 'all' and file.find('%') <> -1:
		sql = sql[:-1] + ' AND model_file_name like (%s);' % listsplit(file)
	
	for row in stg:
		sql = "SELECT count(*) FROM ledger_all_table_columns WHERE project='%s' AND model_file_name='%s' AND table_name='%s';" % (row[0],row[1],row[2])
		
		if int(sqlexecute(sql)[0][0]) == 0: 
			ind = True
			print 'table ' + red(row[2]) + ' in ' + red('%s/%s' % (row[0],row[1])) + ' found no columns'
			
	#validate unique key
	sql = "SELECT project,model_file_name,table_name,column_name,max_length FROM ledger_all_table_columns WHERE unique_key='Y' AND data_type='varchar';"
		
	if file <> 'all' and file.find('%') == -1:
		sql = sql[:-1] + ' AND model_file_name in (%s);' % listsplit(file)
	elif file <> 'all' and file.find('%') <> -1:
		sql = sql[:-1] + ' AND model_file_name like (%s);' % listsplit(file)
	
	stg = sqlexecute(sql)
	
	for row in stg:
		if int(row[4]) > 255:
			ind = True
			print 'table ' + red(row[2]) + ' in ' + red('%s/%s' % (row[0],row[1])) + ' has length=%s' %row[4] + ', the maximun length allowed for a unique key is 255 for a varchar'
	
	#validate decimal data type
	sql = "SELECT project,model_file_name,table_name,column_name,max_length,decimal_place FROM ledger_all_table_columns WHERE data_type='float';"
	
	if file <> 'all' and file.find('%') == -1:
		sql = sql[:-1] + ' AND model_file_name in (%s);' % listsplit(file)
	elif file <> 'all' and file.find('%') <> -1:
		sql = sql[:-1] + ' AND model_file_name like (%s);' % listsplit(file)
		
	stg = sqlexecute(sql)
	
	for row in stg:
		try:
		   int(row[4])
		except ValueError:
		   print 'table ' + red(row[2]) + ' in ' + red('%s/%s' % (row[0],row[1])) + ' has invalid max_length=%s' %row[4]
		   ind = True
		try:
		   int(row[5])
		except ValueError:
		   print 'table ' + red(row[2]) + ' in ' + red('%s/%s' % (row[0],row[1])) + ' has invalid decimal_place=%s' %row[5]
		   ind = True
	
	
	if ind == False: print 'no errors'
	print '\n'
	return
	
##
## function: prepare django model file
## parameter: project name, file name, table name, all_tables field list, all_table_columns field list
## last update: 05/11/09/2016
## 
def write_model_file(p,f,t,tbl,col):
	
	#get tables
	sql = 'SELECT %s FROM ledger_all_tables WHERE project IS NOT NULL AND model_file_name IS NOT NULL AND table_name is NOT NULL;' % listsplit2(tbl)
	
	if p <> 'all': sql = sql[:-1] + " AND project in (%s);" % listsplit(p)
	if f <> 'all': sql = sql[:-1] + " AND model_file_name in (%s);" % listsplit(f)
	if t <> 'all': sql = sql[:-1] + " AND table_name in (%s);" % listsplit(t)
	
	sql = sql[:-1] + ' ORDER BY project, model_file_name, table_name;'
	
	try:
		models = sqlexecute(sql)
	except ValueError, e:
		print sqlerror(e)
		
	tmp1,tmp2,tmp3,tmp4 = ['','',0,'']
		
	for m in models:
		obj_t = Models_t(m,tbl)
		
		if obj_t.project <> tmp1 or obj_t.file <> tmp2:
			print 'prepare script for ' + red('%s/%s' % (obj_t.project,obj_t.file))
			tmp1 = obj_t.project
			tmp2 = obj_t.file
			
			#get file
			obj_f = Models_f(m,tbl)
		
		#get columns
		sql = 'SELECT %s FROM ledger_all_table_columns WHERE project = "%s" AND model_file_name = "%s" AND table_name = "%s";' % (listsplit2(col), obj_t.project.replace(' ','_'), obj_t.file, obj_t.table)
		
		try:
			obj_c = Models_c(sqlexecute(sql),obj_t.table,col)
		except ValueError, e:
			print sqlerror(e)
		
		#get functions
		sql = 'SELECT id,project,model_file_name,table_name,function FROM ledger_all_table_functions WHERE project = "%s" AND model_file_name = "%s" AND table_name = "%s";' % (obj_t.project.replace(' ','_'), obj_t.file, obj_t.table)
		
		try:
			obj_fn = Models_fn(sqlexecute(sql))
		except ValueError, e:
			print sqlerror(e)	
		
		#get script
		model  = obj_t.script.replace(obj_t.p4,obj_c.script + '\n' + obj_fn.script)
		form   = obj_t.form.replace(obj_t.p7,obj_c.form)
		admin  = ''
		backup = obj_t.backup.replace(obj_t.p8,obj_c.backup)
		
		obj_f.setTable(obj_t.table)
		obj_f.setModel(model)
		obj_f.setBackup(backup)
		obj_f.setForm(form)
	
		#save script
		if tmp3 == len(models) - 1: tmp4 = 'Y'
		elif models[tmp3 + 1][tbl.index('project')] <> obj_t.project or models[tmp3 + 1][tbl.index('model file name')] <> obj_t.file: tmp4 = 'Y'
		
		if tmp4 == 'Y':
			print 'update ' + red(obj_t.project + '/__init_.py')
			obj_f.saveInit()
			print 'create ' + red('%s/%s' % (obj_t.project,obj_t.file))
			obj_f.saveFile()
		
		tmp3 = tmp3 + 1
		tmp4 = 'N'

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

def listsplit3(a,b):
	result = ''
	count = 0
	for l in a:			
		result = result + '"' + validate(b[count],str(l)) + '",'
		count = count + 1	
	return result[:-1]

def listsplit4(row,cols):
	b = ""
	for col in cols:
		#if col == 'model file name':
		#	tmp = str(row[cols.index(col)+3])
		#	if tmp.find('.py') == -1:
		#		tmp = tmp + '.py'
		#	b = b + col.replace(' ','_') + ' = "' + tmp + '",'
		#else:
		#	b = b + col.replace(' ','_') + ' = "' + str(row[cols.index(col)+3]) + '",'
		b = b + col.replace(' ','_') + ' = "' + validate(col,row[cols.index(col)+3]) + '",'
	b = b[:-1]
	
	return b
	
def validate(attr,val):
	tmp = str(val).strip()
	
	#if b[count] == 'table name' or b[count] == 'column name': tmp = str(l).upper().replace(' ','_')
	
	if attr == 'model file name':
		tmp = tmp.replace(' ','_')
		if tmp.find('.py') == -1:
			tmp = tmp + '.py'
	
	if attr in cap_list: tmp = tmp.upper()
	
	return tmp

def sqlerror(err):
	result = 'SQL: ' + yellow(str(err[1])) + ' is having error. \nMessage: ' + str(err[0])
	
	if str(err[0][1]).find('Duplicate entry') == 0:
		return '1062'
	else:
		return result

if command == 'loadstaging':
	try:
		f = sys.argv[2]
	except IndexError:
		f = 'all'
	
	loc = 'feeds_IN/map'
	
	if f in ['table','all']:
		t = ['action'] + tbl_list[1:]
		load_stg_table('stg_all_tables',loc,t)
	if f in ['column','all']:
		c = ['action'] + col_list[1:]
		load_stg_table('stg_all_table_columns',loc,c)

if command == 'onlinestaging':
	try:
		f = sys.argv[2]
	except IndexError:
		f = 'all'
		
	if f in ['table','all']:
		t = ['action'] + tbl_list[1:]
		load_stg_table_online('stg_all_tables',t)
	if f in ['column','all']:
		c = ['action'] + col_list[1:]
		load_stg_table_online('stg_all_table_columns',c)
		
elif command == 'insertbase':

	try:
		filter = sys.argv[2]
	except IndexError:
		filter = 'all'
		
	try:
		f = sys.argv[3]
	except IndexError:
		f = 'all'
	
	if f in ['table','all']:
		t = tbl_list[1:]
		load_model_table('all_tables',filter,t)
	if f in ['column','all']:
		c = col_list[1:]
		load_model_table('all_table_columns',filter,c)

elif command == 'validatebase':
	try:
		l = sys.argv[2]
	except IndexError:
		l = 'all'
	
	validate_model_table(l)
		
elif command == 'preparemigration':
	#project name
	try:
		p = sys.argv[2]
	except IndexError:
		p = 'all'
	
	#file name
	try:
		f = sys.argv[3]
	except IndexError:
		f = 'all'
		
	#table name
	try:
		t = sys.argv[4]
	except IndexError:
		t = 'all'
		
	write_model_file(p,f,t,tbl_list[2:],col_list[1:])

elif command == 'makemigration':
	try:
		p = sys.argv[2]
		manage('makemigrations',p)
	except IndexError:
		p = ''
		manage('makemigrations')
	
elif command == 'migrate':
	try:
		p = sys.argv[2]
		manage('migrate',p)
	except IndexError:
		p = ''
		manage('migrate')
		
elif command == 'runserver':
	manage('runserver')
	
elif command == 'buildmodel':
	kwargs = {'project':'all','file':'all','table':'all','column':'','source':'','filter':'all'}
	k=kwargs.copy()
	k.update(dict(x.split('=', 1) for x in sys.argv[2:]))
	
	#load from online staging table
	print (yellow('load from online staging table'))
	if k['source'] in ['table','']:
		tmp = ['action'] + tbl_list[1:]
		load_stg_table_online('stg_all_tables',tmp)
	if k['source'] in ['column','']:
		tmp = ['action'] + col_list[1:]
		load_stg_table_online('stg_all_table_columns',tmp)
		
	#insert into base table
	print (yellow('insert into base table'))
	if k['source'] in ['table','']:
		tmp = tbl_list[1:]
		load_model_table('ledger_all_tables',k['filter'],tmp)
	if k['source'] in ['column','']:
		tmp = col_list[1:]
		load_model_table('ledger_all_table_columns',k['filter'],tmp)
		
	#validate base table
	print (yellow('validate base table'))
	validate_model_table(k['file'])
	
	#prepare migration file
	print (yellow('prepare migration file'))
	write_model_file(k['project'],k['file'],tbl_list[2:],col_list[1:])
	
	#make migration
	print (yellow('make migration'))
	if k['project'] == 'all':
		manage('makemigrations')
	else:
		manage('makemigrations',k['project'])
		
	#migrate
	print (yellow('migrate'))
	if k['project'] == 'all':
		manage('migrate')
	else:
		manage('migrate',k['project'])