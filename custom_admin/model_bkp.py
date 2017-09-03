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
#                                                                              #
################################################################################

import csv
import datetime
import sys
import os

from file import getfile, writefile
from db import sqlexecute
from manage import manage
	
try:
	command = sys.argv[1]
except IndexError:
	command = ''
	
tbl_list = ['id','status','project','model file name','table name','verbose name','verbose name plural','ordering','definition','unicode','model form','backup','retention d','remark']

col_list = ['id','project','table name','model file name','column name','verbose name','verbose name plural','data type','min length','max length','decimal place','path','definition','default value','nullable','blank','unique key','choice options','model form','foreign key table','foreign key column','foreign key on delete','auto save foreign key','remark']
	
def red(self):
	return '\033[91m' + str(self) + '\033[0m'

def yellow(self):
	return '\033[93m' + str(self) + '\033[0m'

def bold(self):
	return '\033[1m' + str(self) + '\033[0m'

class Models_f:
	
	def __init__(self,db,tbl_list):
		self.imp = 'import datetime\nfrom django.db import models\nfrom django.utils import timezone\nfrom django.forms import ModelForm\nfrom django.core.validators import MaxValueValidator, MinValueValidator\n\n'
		
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
				tmp = tmp + '\t' + tmp2
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
					tmp = tmp + '\t' + tmp2
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
				elif self.type == 'DateField':
					tmp = tmp
				
				tmp = tmp + 'null=True,blank=True)\n'
				self.backup = self.backup + tmp
				
				#model columns
				tmp = '\t' + a[col_list.index('column name')] + ' = models.'
				
				if a[col_list.index('foreign key table')] <> '':
					tmp = tmp + "ForeignKey('" + str(a[col_list.index('foreign key table')]) + "',to_field='" + str(a[col_list.index('foreign key column')]) + "',on_delete=models." + str(a[col_list.index('foreign key on delete')]) + ','
					
					if a[col_list.index('auto save foreign key')] == 'Y':
						self.save = self.save + '\t\t' + a[col_list.index('foreign key table')] + '.objects.get_or_create(' + a[col_list.index('foreign key column')] + '=self.' +a[col_list.index('foreign key column')]
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
					
					if self.type == 'DateField' and a[col_list.index('default value')] == 'auto now':
						tmp = tmp + 'auto_now=True,'
					if self.type == 'ImageField':
						tmp = tmp + self.setPicpath(a[col_list.index('project')],a[col_list.index('path')])
					if self.type <> 'DateField' and a[col_list.index('default value')] <> '':
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
				a = ""
				b = ""
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
	
	if filter <> 'all':
		sql = sql[:-1] + ' AND table_name in (%s);' % listsplit(filter);
	
	stg = sqlexecute(sql)
	
	#insert
	if len(stg) == 0:
		print 'no new rows to be updated into %s' % red(tbl)
	else:
		print 'insert into %s...' % red(tbl)
		for row in stg:
			if row[1] == 'add':
				
				sql = "INSERT INTO %s (%s, last_update_date) VALUES (%s,'%s');" % (tbl,a,listsplit3(row[3:],cols),day)
				
				try:
					sqlexecute(sql)
					ids = ids + str(row[0]) + ','
					add_count = add_count + 1
				except ValueError, e:
					if sqlerror(e) == '1062':
						ids_1062 = ids_1062 + str(row[0]) + ','
					
			elif row[1] == 'delete':
				sql = 'DELETE FROM %s WHERE project="%s" AND table_name="%s";' % (tbl,row[cols.index('project')+3],row[cols.index('table name')+3])
				
				if 'column name' in cols:
					sql = sql[:-1] + ' AND column_name="%s";' % row[cols.index('column name')+3]
				
				try:
					sqlexecute(sql)				
					ids = ids + str(row[0]) + ','
					delete_count = delete_count + 1
				except ValueError, e:
					sqlerror(e)
					
			elif row[1] == 'modify':
				'''
				b = ""
				for col in cols:
					b = b + col.replace(' ','_') + ' = "' + str(row[cols.index(col)+3]) + '",'
				b = b[:-1]
				'''
				sql = 'UPDATE %s SET %s, last_update_date = "%s" WHERE project="%s" AND table_name="%s";' % (tbl,listsplit4(row,cols),day,row[cols.index('project')+3],row[cols.index('table name')+3])
				
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
	
def write_model_file(proj,filter,tbl,col):
	
	#get tables
	sql = 'SELECT %s FROM all_tables WHERE project IS NOT NULL AND model_file_name IS NOT NULL AND table_name is NOT NULL;' % listsplit2(tbl)
	
	if proj <> 'all':   sql = sql[:-1] + " AND project in (%s);" % listsplit(proj)
	if filter <> 'all': sql = sql[:-1] + " AND model_file_name in (%s);" % listsplit(filter)
	
	sql = sql[:-1] + ' ORDER BY project, model_file_name;'
	
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
		sql = 'SELECT %s FROM all_table_columns WHERE project = "%s" AND model_file_name = "%s" AND table_name = "%s";' % (listsplit2(col), obj_t.project.replace(' ','_'), obj_t.file, obj_t.table)
		
		try:
			obj_c = Models_c(sqlexecute(sql),obj_t.table,col)
		except ValueError, e:
			print sqlerror(e)
		
		#get script
		model  = obj_t.script.replace(obj_t.p4,obj_c.script)
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
		tmp = str(l)
		#if b[count] == 'table name' or b[count] == 'column name': tmp = str(l).upper().replace(' ','_')
		if b[count] == 'model file name':
			tmp = tmp.replace(' ','_')
			if tmp.find('.py') == -1:
				tmp = tmp + '.py'
			
		result = result + '"' + str(tmp) + '",'
		count = count + 1
	
	return result[:-1]

def listsplit4(row,cols):
	b = ""
	for col in cols:
		if col == 'model file name':
			tmp = str(row[cols.index(col)+3])
			if tmp.find('.py') == -1:
				tmp = tmp + '.py'
			b = b + col.replace(' ','_') + ' = "' + tmp + '",'
		else:
			b = b + col.replace(' ','_') + ' = "' + str(row[cols.index(col)+3]) + '",'
	b = b[:-1]
	
	return b

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
		
elif command == 'preparemigration':
	try:
		p = sys.argv[2]
	except IndexError:
		p = 'all'
	
	try:
		t = sys.argv[3]
	except IndexError:
		t = 'all'
		
	write_model_file(p,t,tbl_list[2:],col_list[1:])

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