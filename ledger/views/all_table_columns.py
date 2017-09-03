from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from ledger.models import all_table_columns, all_tables, all_tables_form, all_table_columns_form, all_table_functions

def tables(request):
	if request.method == 'POST':
		t = request.POST.get('table','')
		i = request.POST.get('id','')
		c = request.POST.get('column','')
		v = request.POST.get('value','')
		
		if t == 'test':
			import sys
			import os
			#sys.path.append('/home/alonglry/personal_finance')
			os.system("python /home/alonglry/personal_finance/custom_admin/proxy_model.py preparemigration ledger account.py")
			return ('ok')
			#if os.system("touch abc.txt") == 0:
				# success
			#else:
				# failure
		elif t == 'tables' and i <> 'new' and v <> 'delete':
			all_tables.update(i,c,v)
			return HttpResponse('%s %s %s %s' % (i,t,c,v))
		elif t == 'columns' and i <> 'new' and v <> 'delete':
			all_table_columns.update(i,c,v)
			return HttpResponse('%s %s %s %s' % (i,t,c,v))
		elif t == 'functions' and i <> 'new' and v <> 'delete':
			all_table_functions.update(i,v)
			return HttpResponse('id: %s table: %s value: %s' % (i,t,v))
		elif t == 'tables' and i <> 'new' and v == 'delete':
			obj = all_tables.objects.get(id=i)
			all_table_columns.objects.filter(table_name=obj.table_name,project=obj.project,model_file_name=obj.model_file_name).delete()
			obj.delete()
			return HttpResponse('ok')
		elif t == 'columns' and i <> 'new' and v == 'delete':
			obj = all_table_columns.objects.get(id=i)
			obj.delete()
			return HttpResponse(i + ' in all_table_columns deleted')
		elif t == 'tables' and i == 'new':
			p = request.POST.get('project','')
			f = request.POST.get('model_file_name','')
			t = request.POST.get('table_name','')
			v = request.POST.get('verbose_name','')
			vp = request.POST.get('verbose_name_plural','')
			o = request.POST.get('ordering','')
			d = request.POST.get('definition','')
			m = request.POST.get('model_form','')
			u = request.POST.get('unicode','')
			b = request.POST.get('backup','')
			r = request.POST.get('retention_d','')
			
			obj = all_tables.add(p,f,t,v,vp,o,d,m,u,b,r)
			
			#convert objects into json
			from django.forms.models import model_to_dict
			dict_obj = model_to_dict(obj)
			import json
			serialized = json.dumps(dict_obj)
			
			return HttpResponse(serialized)
		elif t == 'columns' and i == 'new':
			pj = request.POST.get('project','')
			mfn = request.POST.get('model_file_name','')
			tn = request.POST.get('table_name','')	
			s = request.POST.get('sn','')
			c = request.POST.get('column_name','')
			v = request.POST.get('verbose_name','')
			vp = request.POST.get('verbose_name_plural','')
			d = request.POST.get('definition','')
			dv = request.POST.get('default_value','')
			co = request.POST.get('choice_options','')
			dt = request.POST.get('data_type','')
			mil = request.POST.get('min_length','')
			mal = request.POST.get('max_length','')
			dp = request.POST.get('decimal_place','')
			p = request.POST.get('path','')
			n = request.POST.get('nullable','')
			b = request.POST.get('blank','')
			uk = request.POST.get('unique_key','')
			mf = request.POST.get('model_form','')
			fkt = request.POST.get('foreign_key_table','')
			fkc = request.POST.get('foreign_key_column','')
			fkod = request.POST.get('foreign_key_on_delete','')
			asfk = request.POST.get('auto_save_foreign_key','')
			
			obj = all_table_columns.add(pj,mfn,tn,s,c,v,vp,d,dv,co,dt,mil,mal,dp,p,n,b,uk,mf,fkt,fkc,fkod,asfk)
			
			#convert objects into json
			from django.forms.models import model_to_dict
			dict_obj = model_to_dict(obj)
			import json
			serialized = json.dumps(dict_obj)
			
			return HttpResponse(serialized)
		elif t == 'functions' and i == 'new':
			pj = request.POST.get('project','')
			mfn = request.POST.get('model_file_name','')
			tn = request.POST.get('table_name','')	
			v = request.POST.get('value','')
			
			obj = all_table_functions.add(pj,mfn,tn,v)
			
			#convert objects into json
			from django.forms.models import model_to_dict
			dict_obj = model_to_dict(obj)
			import json
			serialized = json.dumps(dict_obj)
			
			return HttpResponse(serialized)
		elif t == 'files' and i == 'new':
			pj = request.POST.get('project','')
			mfn = request.POST.get('model_file_name','')
			tn = request.POST.get('table_name','')
			c = "python /home/alonglry/personal_finance/custom_admin/proxy_model.py preparemigration %s %s %s" % (pj,mfn,tn)
			
			import os
			return HttpResponse(os.popen(c).read())
			
			#if os.system("touch abc.txt") == 0:
				# success
			#else:
				# failure
	else:
		c = all_table_columns.objects.all()
		t = all_tables.objects.all()
		tf = all_tables_form()
		cf = all_table_columns_form()
		pm = all_tables.get('pm') #project,model_file_name list
		return render(request,'ledger/all_table_columns.html',{'columns':c,
															   'tables':t,
															   'table_form':tf,
															   'column_form':cf,
															   'list':pm})
		
def individual_table(request,table_name):
	if request.method == 'POST':
		t = request.POST.get('table','')
		i = request.POST.get('id','')
		c = request.POST.get('column','')
		v = request.POST.get('value','')
		
		if t == 'tables':
			all_tables.update(i,c,v)
		elif t == 'columns':
			all_table_columns.update(i,c,v)
			
		return HttpResponse('%s %s %s %s' % (i,t,c,v))
			
	else:
		c = all_table_columns.objects.filter(table_name=table_name)
		t = all_tables.objects.filter(table_name=table_name)
		f = all_table_functions.objects.filter(table_name=table_name)
		
		if t:
			return render(request,'ledger/individual_table.html',{'columns':c,'tables':t,'functions':f})
		else:
			return HttpResponseRedirect(reverse('ledger:tables')) 