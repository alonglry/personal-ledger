from datetime import datetime, timedelta
from random import randint
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms

from ledger.models import account_info,journal,ledger,cashflow,parameter
from django.contrib.auth.models import User

#############################################################
# name: trips_journal_form
# type: form
# import by: ledger/view/init
# use: HTML form for trips related transactions
#############################################################
# version author description                      date
# 1.0     awai   initial release                  20/12/2016
# 1.1     awai   add year and month field         04/07/2017
#############################################################

class trips_journal_form(forms.Form):
	trips_activities = (
	('hotel','hotel'),
	('air tickets','air tickets'),
	('commission','commission'),
	)
	payment = (
	('POSB savings','POSB savings'),
	('Citi Dividend','Citi Dividend'),
	)	
	date = forms.DateField(initial=datetime.now().strftime("%Y-%m-%d"))
	year = forms.IntegerField()
	month = forms.IntegerField()
	#choice =  forms.ChoiceField(choices = trips_activities,label='activities')
	destination = forms.CharField(max_length=50)
	activities = forms.CharField(max_length=50)
	currency = forms.CharField(max_length=50,initial='SGD') #widget=forms.TextInput(attrs={'placeholder': 'currency'}))
	amount = forms.DecimalField(max_digits=10, decimal_places=2)
	payment = forms.ChoiceField(choices = payment,label='payment')
	exchange = forms.DecimalField(max_digits=10, decimal_places=2)
	
##############################################################
# name: trips_handler
# type: function
# import by: ledger/urls
# use: main view module for trips related transactions
##############################################################
# version author description                      date
# 1.0     awai   initial release                  20/12/2016
# 1.1     awai   add update source                21/12/2016
# 1.2     awai   remove journal posting           04/06/2017
#                remove date, add year and month
##############################################################

def trips_handler(request):
	if request.method == 'POST':
		#return HttpResponse("Hello world.")
		
		error = ''
		
		try:
			user = User.objects.get(username=request.user.username).first_name
			currency = request.POST.get('currency','')
			activities = request.POST.get('activities','')
			#date = request.POST.get('date','')
			year = request.POST.get('year','')
			month = request.POST.get('month','')
			destination = request.POST.get('destination','')
			payment = request.POST.get('payment','')			
			amount = abs(float(request.POST.get('amount','')))
			exchange = abs(float(request.POST.get('exchange','')))
		except:
			error = error + '\nget variable error'
		
		'''
		if payment == 'POSB savings':
			activity_category = 'cash'
			item_2 = ''
		elif payment == 'Citi Dividend':
			activity_category = 'Citi'
			item_2 = 'Citi'
		elif payment == 'cash':
			activity_category = 'cash'
			item_2 = 'trip'
			
		jrnl = activity_category + str(randint(0,99999))
		'''
		
		
		#update source
		error = error + insert_cashflow(year,month,amount * exchange,user,payment,destination,activities)
		
		try:
			update_account_info(amount * exchange,user,payment)
		except:
			error = error + '\nupdate account info error'
		
		'''
		#update journal
		try:
			insert_journal(date,amount * exchange,user,jrnl,payment,activities,destination)
		except:
			error = error + '\ninsert journal error'
		try:
			ledger.post(jrnl)
		except:
			error = error + '\nupdate ledger error'
		'''
		
		if error == '':
			return HttpResponse('success')
		else:
			return HttpResponse(error)		
	else:
		return HttpResponseRedirect(reverse('ledger:journals'))
		
def insert_cashflow(year,month,amount,user,payment,destination,activities):
	company = 'POSB'
	account = 'savings'
	mode = parameter.mode()
	detail = destination + ' trip - ' + activities
	currency = 'SGD'
	error = ''
	
	'''
	#change date to next month if it's paid after 20th
	if payment == 'Citi Dividend':
		d = datetime.strptime(date, '%Y-%m-%d')
		
		if d.day > 20:
			if d.month == 12:
				date = str(d.year+1) + '-1-1'
			else:
				date = str(d.year) + '-' + str(d.month+1) + '-1'	
	
	if payment == 'POSB savings':
		cashflow.add(date,company,account,'trip',user,-amount,'SGD',jrnl,mode)
	elif payment == 'Citi Dividend':
		cashflow.add(date,company,account,'trip',user,-amount,'SGD',jrnl,mode)
		cashflow.add(date,company,account,'Citi',user,amount,'SGD',jrnl,mode)
	'''
	
	if error == '':
		try:
			cashflow.objects.create(year = year,
														 month = month,
													 company = company,
													 account = account,
															item = 'trip',
														 owner = user,
														amount = -amount,
													currency = currency,
											 #journal_id = jrnl,
														detail = detail,
                		          mode = mode)
		except:
			error = error + '\ninsert_cashflow: inserting cashflow error'
			
	if error == '' and payment == 'Citi Dividend':
		try:
			cashflow.objects.create(year = year,
														 month = month,
													 company = company,
													 account = account,
															item = 'Citi',
														 owner = user,
														amount = amount,
													currency = currency,
											 #journal_id = jrnl,
														detail = detail,
                		          mode = mode)
		except:
			error = error + '\ninsert_cashflow: reversing credit card error'
    	
	return error
		
def update_account_info(amount,user,payment):
	company = 'POSB'
	account = 'savings'
	mode = parameter.mode()
	
	if mode == 'test':
		remark = account_info.objects.get(company=company,identifier=account,owner=user).remark
		if remark == None:
			remark = -amount
		else:
			remark = str(float(remark) - amount)
	else:
		remark = None
	
	if payment == 'POSB savings':
		account_info.update(company,account,user,-amount,remark)

def insert_journal(date,amount,user,jrnl,payment,activities,destination):

	mode = parameter.mode()

	if payment == 'POSB savings':
		ag = 'cash'
		acct1,acct2 = ['POSB savings',None]
		gl1,gl2 = ['POSB savings', 'trip '+get_prev_year(date)]
		ref = activities
		activity = destination + ' trip'
		type1,type2 = ['asset','expense']
		amt1,amt2 = [-amount,amount]
		
		journal.add(date,amt1,'SGD',type1,activity,ag,ref,acct1,gl1,jrnl,user,mode)
		journal.add(date,amt2,'SGD',type2,activity,ag,ref,acct2,gl2,jrnl,user,mode)
	
	if payment == 'Citi Dividend':
		ag = 'credit card'
		acct1,acct2 = [None,None]
		gl1,gl2 = ['Citi '+get_prev_year(date), 'trip '+get_prev_year(date)]
		ref = activities
		activity = destination + ' trip'
		type1,type2 = ['expense','expense']
		amt1,amt2 = [-amount,amount]
		
		journal.add(date,amt1,'SGD',type1,activity,ag,ref,acct1,gl1,jrnl,user,mode)
		journal.add(date,amt2,'SGD',type2,activity,ag,ref,acct2,gl2,jrnl,user,mode)

def get_month(date):
	return datetime.strptime(date, '%Y-%m-%d').strftime('%b')
	
def get_prev_month(date):
	return (datetime.strptime(date, '%Y-%m-%d').replace(day=1)-timedelta(days=1)).strftime('%b')
	
def get_prev_year(date):
	return (datetime.strptime(date, '%Y-%m-%d').replace(day=1)-timedelta(days=1)).strftime('%Y')