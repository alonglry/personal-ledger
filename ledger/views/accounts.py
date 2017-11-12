from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ledger.models import account_info,cashflow,investment_info,investment_transaction,parameter
from django.contrib.auth.models import User
from ledger.utils import user_name, device
from django.db.models import F,Sum,Avg,Max,Min

################################################################
# name: accounts
# type: function
# import by: ledger/urls
# use: main view module for accounts page
################################################################
# version author	description                      		date
# 1.0     awai		initial release											01/01/2017
# 1.1			awai		use basic-nonpost-post structure		15/10/2017
# 1.2     awai    update cashflow logic								23/10/2017
# 1.3			awai		update investment transaction logic	12/11/2017
################################################################

@login_required(login_url='/login/')
def accounts(request):
	
	try:
		d = device(request)
	except Exception as err:
		return render(request,'ledger/error_page.html',{'device':'phone','message':err.args[0]})	

	try:
		user = user_name(request)
	except Exception as err:
		return render(request,'ledger/error_page.html',{'device':d,'message':err.args[0]})
	
	if request.method <> 'POST':
		
		error = ''
		
		#get account info
		try:
			ai = account_info.objects.filter(owner=user).exclude(type = 'shares').exclude(type='funds')
		except:
			error = error + '\naccount_info get value having issue.'
		
		#get cashflow
		try:
			c = cashflow.objects.filter(account_info__in=ai)
		except:
			error = error + '\ncashflow get value having issue.'
		
		#use account info and cashflow to prepare data for template
		try:
			l1 = []
			'''
			i = c.order_by('item').values('item').distinct()
			f = c.order_by('company','account','owner','account_info','item','year','month','currency').values('company','account','owner','account_info','item','year','month','currency').annotate(amount = Sum('amount'))			
			d = c.order_by('year','month').values('year','month').distinct()			
			
			l.append([i,d,f])
			
			#c = cashflow.get('all',account_info.get('cao',user))
			'''
			
			for a in ai:
				ll = []
				i = c.filter(account_info=a).order_by('item').values('item').distinct()
				d = c.filter(account_info=a).order_by('year','month').values('year','month').distinct()
				f = c.filter(account_info=a).order_by('item','year','month','currency').values('item','year','month','currency').annotate(amount = Sum('amount'))
				
				ll.append(a)
				ll.append(i)
				ll.append(d)
				ll.append(f)
				
				l1.append(ll)
				
		except:
			error = error + '\ncashflow prepare data having issue.'
		
		#get investment info
		try:
			ii = investment_info.objects.filter(owner=user).exclude(identifier = '')
		except:
			error = error + '\ninvestment info get value having issue.'
		
		#get investment transaction
		try:
			#it = investment_transaction.get_transaction('all',investment_info.get('cao',user))
			it = investment_transaction.objects.filter(investment_info__in=ii,transaction_type_1='actual')
		except:
			error = error + '\investment transaction get value having issue.'
			
		#use investment info and investment transaction to prepare data for template
		try:
			l2 = []
			
			for a in ii:
				ll = []
				
				i = it.filter(investment_info=a).order_by('transaction_type_2').values('transaction_type_2').distinct()
				d = it.filter(investment_info=a).order_by('date').values('date').distinct()
				f = it.filter(investment_info=a).order_by('transaction_type_2','date')	
				
				ll.append(a)
				ll.append(i)
				ll.append(d)
				ll.append(f)
				
				l2.append(ll)
				
		except:
			error = error + '\ninvestment_transaction prepare data having issue.'

		try:
			
			sum = 0
			
			for a in ii:
				u = float(a.unit)
				p = float(a.price)
				
				sum = sum + u * p
				
		except:
			error = error + '\ninvestment info get total sum having issue.'

		if error == '':
			return render(request,'ledger/accounts.html',{'acct':ai.order_by('company','identifier'),
																								 'company':ai.values('company').distinct(),
																									 	  'cf':l1,
																						 'investments':ii,
																						 'transaction':l2,
																										'user':user,
																				'total_investment':sum,
																									'device':d
															})
		else:
			#return HttpResponse(error)
			return render(request,'ledger/error_page.html',{'device':d,'message':error})
		
	else:
		return render(request,'ledger/error_page.html',{'device':d,'message':'This page has no POST request'})