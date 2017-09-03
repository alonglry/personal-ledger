from django.db import connection
from collections import namedtuple
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ..forms import sql_form
import sys
from ..utils import sql_save,sql_get,sql_truncate
from django.contrib.auth.decorators import login_required

def execsql(sql):
	cursor = connection.cursor()
	try:
		cursor.execute(sql)
		result = cursor.fetchall()
		try:
			desc = cursor.description
			nt_result = namedtuple('Result', [col[0] for col in desc])
			return [col[0] for col in desc],[nt_result(*row) for row in result]
			#columns = [col[0] for col in cursor.description]
			#return [
			#	dict(zip(columns, row))
			#	for row in result
			#]
		except:
			return [''],result
	except Exception, e:
		#exc_type, exc_value, exc_traceback = sys.exc_info()
		#return 'error',exc_type.__name__.replace('Error',' Error') + ': ' + exc_value.message
		return 'error', str(e)
		
@login_required(login_url='/login/')
def sql_handler(request):
	#return HttpResponse("Hello, world. strategies")
	user = request.user.username
	if request.method == 'POST' :
		sql = get_sql(request.POST.get('input',''))
		desc,result = execsql(sql)
		sql = sql_get()
		
		if desc <> 'error':
			return render(request,'ledger/sql.html',{'textbox':sql_form(),'data':result,'desc':desc,'sql':sql,'user':user})
		else:
			return render(request,'ledger/sql.html',{'textbox':sql_form(),'sql':sql,'error':result,'user':user})
	else:
		sql_truncate()
		return render(request,'ledger/sql.html',{'textbox':sql_form(),'user':user})
		
col = 'project,model_file_name,table_name,column_name,verbose_name,verbose_name_plural,data_type,min_length,max_length,decimal_place,path,definition,default_value,nullable,blank,unique_key,choice_options,model_form,foreign_key_table,foreign_key_column,foreign_key_on_delete,auto_save_foreign_key,remark'

def get_sql(sql):
	if sql.find('stg_all_table_colmuns') <> -1 or sql[:1] == '1':
		a = sql.split()
		c = len(a)
		if c == 1:
			tmp = 'SELECT id,action,status, %s FROM stg_all_table_columns ORDER by project,model_file_name,table_name,column_name;' % col
		if c == 2:
			if a[1].find('%'):
				tmp = "SELECT id,action,status,%s FROM stg_all_table_columns WHERE project LIKE '%s' OR model_file_name LIKE '%s' OR table_name LIKE '%s' ORDER by project,model_file_name,table_name,column_name;" % (col,a[1],a[1],a[1])
			else:
				tmp = "SELECT id,action,status,%s FROM stg_all_table_columns WHERE project IN (%s) OR model_file_name IN (%s) OR table_name IN (%s) ORDER by project,model_file_name,table_name,column_name;" % (col,splitlist(a[1]),splitlist(a[1]),splitlist(a[1]))
	elif sql.find('all_table_colmuns') <> -1 or sql[:1] == '2':
		a = sql.split()
		c = len(a)
		if c == 1:
			tmp = 'SELECT id,%s FROM all_table_columns ORDER by project,model_file_name,table_name,column_name;' % col
		if c == 2:
			if a[1].find('%'):
				tmp = "SELECT id,%s FROM all_table_columns WHERE project LIKE '%s' OR model_file_name LIKE '%s' OR table_name LIKE '%s' ORDER by project,model_file_name,table_name,column_name;" % (col,a[1],a[1],a[1])
			else:
				tmp = "SELECT id,%s FROM all_table_columns WHERE project IN (%s) OR model_file_name IN (%s) OR table_name IN (%s) ORDER by project,model_file_name,table_name,column_name;" % (col,splitlist(a[1]),splitlist(a[1]),splitlist(a[1]))
	else:
		tmp = sql
		sql_save(sql)
		
	return tmp
				
def split_list(list):
	a = list.split(',')
	t = ''
	for aa in a:
		t = t + "'" + aa + "',"
	return t[:-1]