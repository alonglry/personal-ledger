from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ledger.models import account_info,cashflow,investment_info,investment_transaction,parameter
from ledger.utils import user_name, device
from ledger.forms import transaction_form

##############################################################
# name: transactions
# type: function
# import by: ledger/urls
#            ledger/views/_init_.py
# use: main view module for transaction (from source) page
##############################################################
# version author description                      date
# 1.0     awai   initial release                  23/07/2017
###############################################################

@login_required(login_url='/login/')
def transaction(request):
	
	try:
		d = device(request)
	except Exception as err:
		return render(request,'ledger/error_page.html',{'device':'phone','message':err.args[0]})	
	
	try:
		user = user_name(request)
	except Exception as err:
		return render(request,'ledger/error_page.html',{'device':d,'message':err.args[0]})
  
	return render(request,'ledger/transaction.html',{'device':d,'textbox':transaction_form(),'user':user})

	
'''
	if request.method == 'POST':
    1=1
  else:
    return render(request,'ledger/transactions.html',{'textbox':sql_form(),'user':user})
    
'''