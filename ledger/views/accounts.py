from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ledger.models import account_info,cashflow,investment_info,investment_transaction,parameter
from django.contrib.auth.models import User

##############################################################
# name: accounts
# type: function
# import by: ledger/urls
# use: main view module for accounts page
##############################################################
# version author description                      date
# 1.0     awai   initial release                  01/01/2017
##############################################################

@login_required(login_url='/login/')
def accounts(request):
	if request.META.get('HTTP_USER_AGENT', '').lower().find("iphone") > 0:
		device = 'phone'
	else:
		device = 'others'
		
	error = ''
	
	try:
		user = User.objects.get(username=request.user.username).first_name
	except:
		error = error + '\nuser not able to find last name.'
		
	try:
		account_info.get('cao',user)
	except:
		error = error + '\naccount_info get company, account, owner having issue.'
	
	try:
		c = cashflow.get('all',account_info.get('cao',user))
	except:
		error = error + '\ncashflow get company, account, owner having issue.'
		
	try:
		i = investment_info.get('all',user)
	except:
		error = error + '\ninvestment info get account having issue.'
		
	try:
		it = investment_transaction.get_transaction('all',investment_info.get('cao',user))
	except:
		error = error + '\investment transaction get transaction having issue.'
	
	try:
		sum = investment_info.sum_current_amount(user)
	except:
		error = error + '\ninvestment info get total sum having issue.'
	
	if error == '':
		return render(request,'ledger/accounts.html',{'acct':account_info.get('all',user),
													  'company':account_info.get('company',user),
													  'cf':cashflow.get('all',account_info.get('cao',user)),
													  'investments':i,
													  'transaction':it,
													  'user':request.user.username,
													  'total_investment':sum,
													  'device':device
													  })
	else:
		return HttpResponse(error)