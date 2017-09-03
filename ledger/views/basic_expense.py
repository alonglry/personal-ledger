from datetime import datetime, timedelta
from random import randint
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from ledger.models import account_info,cashflow,journal,ledger,parameter
from django.contrib.auth.models import User
from django import forms
	
#############################################################
# name: basic_journal_form
# type: form
# import by: NA
# use: HTML form for basic expense related transactions
#############################################################
# version author description                      date
# 1.0     awai   initial release                  21/12/2016
# 1.1 		awai   remove import of this form
#############################################################

class basic_journal_form(forms.Form):
	journal_activities = (
	('salary','salary'),
	('rental','rental'),
	('4G','4G'),
	('Citi dividend','Dividend Card')
	)
	date = forms.DateField(initial=datetime.now().strftime("%Y-%m-%d"))
	#choice = forms.ChoiceField(choices = journal_activities,label='activities')
	choice = forms.CharField(max_length=50,required = False)
	amount = forms.DecimalField(max_digits=10, decimal_places=2)
	#initial=datetime.date time.now().strftime("%Y-%m-%d"),

##############################################################
# name: basic_expense_handler
# type: function
# import by: ledger/urls
# use: main view module for basic expense related transactions
##############################################################
# version author description                      date
# 1.0     awai   initial release                  20/12/2016
# 1.1     awai	 add test mode                    06/02/2017
#                remove journal    
# 1.2     awai   update insert_cashflow           05/03/2017
# 1.3     awai   add year, month column           21/05/2017
##############################################################

def basic_expense_handler(request):
	if request.method == 'POST':
		#return HttpResponse("Hello, world. cpf")
		
		error = ''
		
		#get variable
		try:		
			year = request.POST.get('year','')
			month = request.POST.get('month','')
			jrnl = 'cash' + str(randint(0,99999))
			amt = float(request.POST.get('amount',''))
			item = request.POST.get('choice','')
			user = User.objects.get(username=request.user.username).first_name
		except:
			error = error + '\nget variable error'
		
		#update source
		error = error + insert_cashflow(amt,item,user,year,month,jrnl)
			
		try:
			update_account_info(amt,item,user)
		except:
			error = error + '\nupdate account info error'
			
		#insert_journal(date,item,amt,user,jrnl)
		#ledger.post(jrnl)
			
		if error == '':
			return HttpResponse('success')
		else:
			return HttpResponse(error)
	else:
		return HttpResponseRedirect(reverse('ledger:journals'))
		
def insert_cashflow(amt,item,user,year,month,jrnl):
	
	company  = 'POSB'
	account  = 'savings'
	currency = 'SGD'
	amt      = amt if item == 'salary' else -amt
	mode     = parameter.mode()
	error    = ''
	
	'''
	try:
		#get previous month and year if it's payment to credit card, phone, rental
		month = (datetime.strptime(date, '%Y-%m-%d').replace(day=1)-timedelta(days=1)).strftime('%m') if item in ['Citi','4G'] else datetime.strptime(date,'%Y-%m-%d').strftime('%m')
		year  = (datetime.strptime(date, '%Y-%m-%d').replace(day=1)-timedelta(days=1)).strftime('%Y') if (item in ['Citi','4G'] and datetime.strptime(date,'%Y-%m-%d').strftime('%m') == '01') else datetime.strptime(date,'%Y-%m-%d').strftime('%Y')
	except:
		error = error + '\ninsert_cashflow: getting year and month error'	
	'''
	#cashflow.add(date,company,account,item,user,amt,'SGD',jrnl,mode)
	
	if error == '':
		try:
			cashflow.objects.create(year = year,
														 month = month,
													 company = company,
													 account = account,
															item = item,
														 owner = user,
														amount = amt,
													currency = currency,
												journal_id = jrnl,
                		          mode = mode)
		except:
			error = error + '\ninsert_cashflow: inserting cashflow error'
    	
	return error

	
def update_account_info(amt,item,user):
	company = 'POSB'
	account = 'savings'
	amt = amt if item == 'salary' else -amt
	mode = parameter.mode()
	
	if mode == 'test':
		remark = account_info.objects.get(company=company,identifier=account,owner=user).remark
		
		if remark == None:
			remark = amt
		else:
			remark = str(float(remark) + amt)
	else:
		remark = None
	
	account_info.update(company,account,user,amt,remark)
	
def insert_journal(date,item,amt,user,jrnl):
	ag = 'cash'
	acct1,acct2 = ['POSB savings',None]
	gl1,gl2 = ['POSB savings', item + ' '+get_prev_year(date)]
	ref = item + '-' + str(get_prev_month(date)) + ' ' + str(get_prev_year(date))
	activity = item
	
	if item == 'salary':
		type1,type2 = ['asset','income']
		amt1,amt2 = [amt,-amt]
	else:
		type1,type2 = ['asset','expense']
		amt1,amt2 = [-amt,amt]
		
	journal.add(date,amt1,'SGD',type1,activity,ag,ref,acct1,gl1,jrnl,user)
	journal.add(date,amt2,'SGD',type2,activity,ag,ref,acct2,gl2,jrnl,user)
	
def get_month(date):
	return datetime.strptime(date, '%Y-%m-%d').strftime('%b')
	
def get_prev_month(date):
	return (datetime.strptime(date, '%Y-%m-%d').replace(day=1)-timedelta(days=1)).strftime('%b')
	
def get_prev_year(date):
	return (datetime.strptime(date, '%Y-%m-%d').replace(day=1)-timedelta(days=1)).strftime('%Y')