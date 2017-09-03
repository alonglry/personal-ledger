'''from ..models import journal, ledger
from datetime import datetime
from account import account_balance_update
from django.db.models import F

from parameter import ledger_posting
#from django.http import HttpResponse

def get_date(request):
	return request.POST.get('date','')
	
def get_year(date):
	return datetime.strptime(date, '%Y-%m-%d').strftime('%Y')

def get_month(date):
	return datetime.strptime(date, '%Y-%m-%d').strftime('%m')
	
def journal_post(jrnl):
	j = journal.objects.filter(journal_id=jrnl,post_indicator__isnull=True)
	
	for o in j:
		#return HttpResponse(o.account_id)
		try:
			ledger.objects.update_or_create(gl_account = o.gl_account, account_id = o.account_id,
										balancesheet_type = o.balancesheet_type, currency = o.currency,
												 activity = o.activity, activity_category = o.activity_category,
												 defaults = {'amount':F('amount')+o.amount})
		except:
			ledger(gl_account = o.gl_account, account_id = o.account_id,
			   balancesheet_type = o.balancesheet_type, 
						  amount = o.amount, currency = o.currency,
						activity = o.activity, activity_category = o.activity_category).save()
		
	j.update(post_indicator='Y')
		
def journal_add(d,a,c,b,ac,acc,r,ai,g,j):
	if a <> 0:
		journal( date = d,
				 year = get_year(d),
				month = get_month(d),
			   amount = a,
			 currency = c,
	balancesheet_type = b,
			 activity = ac,
	activity_category = acc,
			reference = r,
		   account_id = ai,
		   gl_account = g,
		   journal_id = j
			   ).save()
			   
		#update account balance	   
		if ai == 'POSB savings':
			account_balance_update('POSB savings',a)
		elif ai == 'vickers deposit':
			account_balance_update('vickers deposit',a)
		elif ai == 'CPF ordinary':
			account_balance_update('CPF ordinary',a)
		elif ai == 'CPF special':
			account_balance_update('CPF special',a)
		elif ai == 'CPF medisave':
			account_balance_update('CPF medisave',a)

def ledger_add(journal):
	if ledger_posting():
		try:
			ledger.objects.update_or_create(gl_account_id = journal.gl_account_id, account_id = journal.account_id,
										balancesheet_type = journal.balancesheet_type, currency = journal.currency,
												 activity = journal.activity,
												 defaults = {'amount':F('amount')+journal.amount})
		except:
			ledger(gl_account_id = journal.gl_account_id, account_id = journal.account_id,
			   balancesheet_type = journal.balancesheet_type, 
						  amount = journal.amount, currency = journal.currency,
						activity = journal.activity).save()

def n(item):
	t = n
	if n is None:
		t = ''
	return t
'''