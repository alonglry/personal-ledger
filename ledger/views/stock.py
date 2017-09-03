import sys
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from ledger.utils import stock_get,stock_save

def stock_handler(request):
	#return HttpResponse("Hello, world. strategies")
	if request.method == 'POST' and getValue(request,'name') == 'company':
		stock_save(request,'company')
		return HttpResponseRedirect(reverse('ledger:stocks'))
	else:
		return render(request,'ledger/stocks.html',{'company_verbose': stock_get('company_meta'),
													'company_all'    : stock_get('company_all'),
													'company_form'   : stock_get('company_form')})

def getValue(request,field):
	tmp = None if request.POST.get(field,'') == '' else request.POST.get(field,'')
	return tmp