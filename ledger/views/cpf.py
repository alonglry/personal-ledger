from datetime import datetime, timedelta
from random import randint
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms

from ledger.models import account_info,cashflow,journal,ledger,parameter
from django.contrib.auth.models import User

#############################################################
# name: dbs_cpf_journal_form
# type: form
# import by: ledger/view/init
# use: HTML form for CPF related transactions
#############################################################
# version author description                      date
# 1.0     awai   initial release                  30/01/2017
#############################################################
class cpf_journal_form(forms.Form):
	date = forms.DateField(initial=datetime.now().strftime("%Y-%m-%d"))
	ordinary = forms.DecimalField(initial=953.69, max_digits=10, decimal_places=2,required = False)
	special = forms.DecimalField(initial=248.66, max_digits=10, decimal_places=2,required = False)
	medisave = forms.DecimalField(initial=331.65, max_digits=10, decimal_places=2,required = False)
	medishield = forms.DecimalField(max_digits=10, decimal_places=2,required = False)
	dps = forms.DecimalField(max_digits=10, decimal_places=2,required = False)
	
##############################################################
# name: cpf_handler
# type: function
# import by: ledger/urls
# use: main view module for CPF related transactions
##############################################################
# version author description                      date
# 1.0     awai   initial release                  30/01/2017
# 1.1     awai   remove journal                   05/03/2017
#                add test mode
#                add error handling
##############################################################
def cpf_handler(request):
	if request.method == 'POST':
		#return HttpResponse("Hello, world. cpf")
		
		error = ''
		
		try:
			#get variables
			ordinary = float(request.POST.get('ordinary',''))
			special = float(request.POST.get('special',''))
			medisave = float(request.POST.get('medisave',''))
			medishield = 0 if request.POST.get('medishield','') == '' else float(request.POST.get('medishield',''))
			dps = 0 if request.POST.get('dps','') == '' else float(request.POST.get('dps',''))
			date = request.POST.get('date','')
			jrnl = 'cpf' + str(randint(0,99999))
			user = User.objects.get(username=request.user.username).first_name
		except:
			error = error + '\nget variable error'
		
		if error == '':
			error = error + insert_cashflow(ordinary,special,medisave,medishield,dps,user,date,jrnl)
		if error == '':
			error = error + update_account_info(ordinary,special,medisave,medishield,dps,user)
		#insert_journal(ordinary,special,medisave,medishield,dps,user,date,jrnl)
		#ledger.post(jrnl)
		
		if error == '':
			return HttpResponse('success')
		else:
			return HttpResponse(error)
	else:
		return HttpResponseRedirect(reverse('ledger:journals'))
		
def insert_cashflow(ordinary,special,medisave,medishield,dps,user,date,jrnl):
	
	year  = (datetime.strptime(date, '%Y-%m-%d').replace(day=1)-timedelta(days=1)).strftime('%Y') if datetime.strptime(date,'%Y-%m-%d').strftime('%m') == '01' else datetime.strptime(date,'%Y-%m-%d').strftime('%Y')
	month = (datetime.strptime(date, '%Y-%m-%d').replace(day=1)-timedelta(days=1)).strftime('%m')
	item = 'INT' if ordinary < 200 else 'CON'
	mode  = parameter.mode()
	error = ''
	
	#ordinary
	#cashflow.add(date,'CPF','ordinary',item,user,ordinary,'SGD',jrnl)
	#cashflow.add(date,'CPF','ordinary','DPS',user,-dps,'SGD',jrnl)
	try:
		cashflow.objects.create(date = date,
								year = year,
							   month = month,
							 company = 'CPF',
							 account = 'ordinary',
								item = item,
							   owner = user,
							  amount = ordinary,
							currency = 'SGD',
						  journal_id = jrnl,
               		            mode = mode)
	except:
		error = error + '\ninsert_cashflow: inserting ordinary error'
	
	try:
		cashflow.objects.create(date = date,
								year = year,
							   month = month,
							 company = 'CPF',
							 account = 'DPS',
								item = item,
							   owner = user,
							  amount = -dps,
							currency = 'SGD',
						  journal_id = jrnl,
               		            mode = mode)
	except:
		error = error + '\ninsert_cashflow: inserting DPS error'	
		
	
	#special
	#cashflow.add(date,'CPF','special',item,user,special,'SGD',jrnl)
	try:
		cashflow.objects.create(date = date,
								year = year,
							   month = month,
							 company = 'CPF',
							 account = 'special',
								item = item,
							   owner = user,
							  amount = special,
							currency = 'SGD',
						  journal_id = jrnl,
               		            mode = mode)
	except:
		error = error + '\ninsert_cashflow: inserting special error'
		
	#medisave
	#cashflow.add(date,'CPF','medisave',item,user,medisave,'SGD',jrnl)
	#cashflow.add(date,'CPF','medisave','MSL',user,-medishield,'SGD',jrnl)
	try:
		cashflow.objects.create(date = date,
								year = year,
							   month = month,
							 company = 'CPF',
							 account = 'medisave',
								item = item,
							   owner = user,
							  amount = medisave,
							currency = 'SGD',
						  journal_id = jrnl,
               		            mode = mode)
	except:
		error = error + '\ninsert_cashflow: inserting medisave error'
		
	try:
		cashflow.objects.create(date = date,
								year = year,
							   month = month,
							 company = 'CPF',
							 account = 'medisave',
								item = item,
							   owner = user,
							  amount = -medishield,
							currency = 'SGD',
						  journal_id = jrnl,
               		            mode = mode)
	except:
		error = error + '\ninsert_cashflow: inserting MSL error'
		
	return error
		
def update_account_info(ordinary,special,medisave,medishield,dps,user):
	mode = parameter.mode()
	error = ''
	
	try:
		#ordinary
		if mode == 'test':
			remark = account_info.objects.get(company='CPF',identifier='ordinary',owner=user).remark
			
			if remark == None:
				remark = ordinary - dps
			else:
				remark = str(float(remark) + ordinary - dps)
		else:
			remark = None
		
		account_info.update('CPF','ordinary',user,ordinary - dps,remark)
	except:
		error = error + '\nupdate_account_info: update ordinary error'
	
	try:
		#special
		if mode == 'test':
			remark = account_info.objects.get(company='CPF',identifier='special',owner=user).remark
		
			if remark == None:
				remark = special
			else:
				remark = str(float(remark) + special)
		else:
			remark = None
	
		account_info.update('CPF','special',user,special,remark)
	except:
		error = error + '\nupdate_account_info: update special error'
	
	try:
		#medisave
		if mode == 'test':
			remark = account_info.objects.get(company='CPF',identifier='medisave',owner=user).remark
		
			if remark == None:
				remark = medisave - medishield
			else:
				remark = str(float(remark) + medisave - medishield)
		else:
			remark = None
		
		account_info.update('CPF','medisave',user,medisave - medishield,remark)
	except:
		error = error + '\nupdate_account_info: update medisave error'
		
	return error
	
def insert_journal(ordinary,special,medisave,medishield,dps,user,date,jrnl):
	#ordinary
	ac = 'ordinary account contribution' if ordinary > 100 else 'CPF ordinary account interest'
	ref = 'CPF-' + str(get_prev_month(date)) + ' ' + str(get_prev_year(date))
	journal.add(date,ordinary,'SGD','asset',ac,'CPF',ref,'CPF ordinary','CPF ordinary',jrnl,user)
	journal.add(date,-ordinary,'SGD','income',ac,'CPF',ref,'','CPF ' + str(get_prev_year(date)),jrnl,user)
	
	ac = 'Dependants\' Protection Scheme'
	ref = 'CPF-' + str(get_prev_month(date)) + ' ' + str(get_prev_year(date))
	journal.add(date,-dps,'SGD','asset',ac,'CPF',ref,'CPF ordinary','CPF ordinary',jrnl,user)
	journal.add(date,dps,'SGD','expense',ac,'CPF',ref,'','insurance ' + str(get_prev_year(date)),jrnl,user)
	
	#special
	ac = 'special account contribution' if ordinary > 100 else 'CPF special account interest'
	ref = 'CPF-' + str(get_prev_month(date)) + ' ' + str(get_prev_year(date))
	journal.add(date,special,'SGD','asset',ac,'CPF',ref,'CPF special','CPF special',jrnl,user)
	journal.add(date,-special,'SGD','income',ac,'CPF',ref,'','CPF ' + str(get_prev_year(date)),jrnl,user)
	
	#medisave
	ac = 'medisave account contribution' if ordinary > 100 else 'CPF medisave account interest'
	ref = 'CPF-' + str(get_prev_month(date)) + ' ' + str(get_prev_year(date))
	journal.add(date,medisave,'SGD','asset',ac,'CPF',ref,'CPF medisave','CPF medisave',jrnl,user)
	journal.add(date,-medisave,'SGD','income',ac,'CPF',ref,'','CPF ' + str(get_prev_year(date)),jrnl,user)
	
	ac = 'MediShield Life'
	ref = 'CPF-' + str(get_prev_month(date)) + ' ' + str(get_prev_year(date))
	journal.add(date,-medishield,'SGD','asset',ac,'CPF',ref,'CPF medisave','CPF medisave',jrnl,user)
	journal.add(date,medishield,'SGD','expense',ac,'CPF',ref,'','insurance ' + str(get_prev_year(date)),jrnl,user)

def number(request,item):
	n = request.POST.get(item,'')
	if n is None or n == '':
		n = 0
	n = float(n)
	return n
	
def get_month(date):
	return datetime.strptime(date, '%Y-%m-%d').strftime('%b')
	
def get_prev_month(date):
	return (datetime.strptime(date, '%Y-%m-%d').replace(day=1)-timedelta(days=1)).strftime('%b')
	
def get_prev_year(date):
	return (datetime.strptime(date, '%Y-%m-%d').replace(day=1)-timedelta(days=1)).strftime('%Y')