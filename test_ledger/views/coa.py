import sys
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from test_ledger.utils import get_acct_rollup, save_acct_rollup

def coa_handler(request):
	if request.method == 'POST':
		save_acct_rollup(request)
		return HttpResponseRedirect(reverse('test_ledger:coa'))
	else:
		return render(request,'test_ledger/coa.html',{'coa':      get_acct_rollup('all'),
													  'verbose':  get_acct_rollup('meta'),
													  'coa_form': get_acct_rollup('form')})