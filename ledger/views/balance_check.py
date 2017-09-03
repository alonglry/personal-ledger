from datetime import datetime, timedelta
from random import randint
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from itertools import chain

from ledger.models import account_info,cashflow,journal,ledger,investment_info

@login_required(login_url='/login/')
def balance_check_handler(request):
	user = request.user.username
	j = journal.get('checkbs',user)
	l = ledger.get('checkbs',user)
	a = list(chain(account_info.get('checkbs',user),investment_info.get('checkbs',user)))
	c = cashflow.get('checkbs','',user)
	
	j2 = journal.get('checkpl',user)
	l2 = ledger.get('checkpl',user)
	
	return render(request,'ledger/check.html',{'journal':j,'ledger':l,'account':a,'cashflow':c,
											   'journalpl':j2,'ledgerpl':l2,
											   'user':user})