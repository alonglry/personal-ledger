'''from datetime import datetime
from random import randint

from ..utils.ledger import get_date, journal_add, journal_post, get_year
from ..utils.cashflow import add_cashflow

def basic_handler(request):

	date = get_date(request)
	jrnl = 'cash' + str(randint(0,99999))
	amt = float(request.POST.get('amount',''))
	choice = request.POST.get('choice','')
	year = get_year(date)
	
	a_1 = gl_1 = 'POSB savings'
	gl_2 = choice + ' ' + str(year)
	a_2 = None
	ref = choice + '-' + str(get_month(date)) + ' ' + str(get_year(date))
	t1 = 'asset'
	t2 = 'income' if choice == 'salary' else 'expense'
	amt = amt if choice == 'salary' else -amt
	
	add_cashflow(date,choice,amt)
	
	journal_add(date,amt,'SGD',t1,choice,'cash',ref,a_1,gl_1,jrnl)
	journal_add(date,-amt,'SGD',t2,choice,'cash',ref,a_2,gl_2,jrnl)
	journal_post(jrnl)
	
def journal_handler(request):
	date = get_date(request)
	jrnl = request.POST.get('journal_id','')
	amt = float(request.POST.get('amount',''))
	ac = request.POST.get('activity','')
	acg = request.POST.get('activity_category','')
	jrnl = acg + str(randint(0,99999)) if jrnl == '' else jrnl
	ccy = request.POST.get('currency','')
	ref = request.POST.get('reference','')
	
	t_1 = request.POST.get('balancesheet_type_1','')
	t_2 = request.POST.get('balancesheet_type_2','')
	a_1 = request.POST.get('account_id_1','')
	a_2 = request.POST.get('account_id_2','')
	gl_1 = request.POST.get('gl_account_1','')
	gl_2 = request.POST.get('gl_account_2','')
	
	if gl_1 <> '':	
		journal_add(date,amt,ccy,t_1,ac,acg,ref,a_1,gl_1,jrnl)
	if gl_2 <> '':
		journal_add(date,-amt,ccy,t_2,ac,acg,ref,a_2,gl_2,jrnl)
	
	journal_post(jrnl)
	
def get_month(date):
	return datetime.strptime(date, '%Y-%m-%d').strftime('%b')
'''