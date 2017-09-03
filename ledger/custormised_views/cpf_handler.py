'''

from django.http import HttpResponse
from datetime import datetime
from random import randint

from ..utils.ledger import get_date, journal_add, journal_post, get_year

def cpf_handler(request):
	ordinary = number(request,'ordinary')
	special = number(request,'special')
	medisave = number(request,'medisave')
	medishield = number(request,'medishield')
	dps = number(request,'dps')
	date = get_date(request)
	jrnl = 'cpf' + str(randint(0,99999))
	
	#ordinary account
	ac = 'ordinary account contribution' if ordinary > 100 else 'CPF ordinary account interest'
	ref = 'CPF-' + str(get_month(date)) + ' ' + str(get_year(date))
	journal_add(date,ordinary,'SGD','asset',ac,'CPF',ref,'CPF ordinary','CPF ordinary',jrnl)
	journal_add(date,-ordinary,'SGD','income',ac,'CPF',ref,'','CPF ' + str(get_year(date)),jrnl)
	
	#special account
	ac = 'special account contribution' if ordinary > 100 else 'CPF special account interest'
	ref = 'CPF-' + str(get_month(date)) + ' ' + str(get_year(date))
	journal_add(date,special,'SGD','asset',ac,'CPF',ref,'CPF special','CPF special',jrnl)
	journal_add(date,-special,'SGD','income',ac,'CPF',ref,'','CPF ' + str(get_year(date)),jrnl)
	
	#medisave account
	ac = 'medisave account contribution' if ordinary > 100 else 'CPF medisave account interest'
	ref = 'CPF-' + str(get_month(date)) + ' ' + str(get_year(date))
	journal_add(date,medisave,'SGD','asset',ac,'CPF',ref,'CPF medisave','CPF medisave',jrnl)
	journal_add(date,-medisave,'SGD','income',ac,'CPF',ref,'','CPF ' + str(get_year(date)),jrnl)
	
	#Dependants' Protection Scheme
	ac = 'Dependants\' Protection Scheme'
	ref = 'CPF-' + str(get_month(date)) + ' ' + str(get_year(date))
	journal_add(date,-dps,'SGD','asset',ac,'CPF',ref,'CPF ordinary','CPF ordinary',jrnl)
	journal_add(date,dps,'SGD','expense',ac,'CPF',ref,'','insurance ' + str(get_year(date)),jrnl)
	
	#MediShield Life
	ac = 'MediShield Life'
	ref = 'CPF-' + str(get_month(date)) + ' ' + str(get_year(date))
	journal_add(date,-medishield,'SGD','asset',ac,'CPF',ref,'CPF medisave','CPF medisave',jrnl)
	journal_add(date,medishield,'SGD','expense',ac,'CPF',ref,'','insurance ' + str(get_year(date)),jrnl)
	
	journal_post(jrnl)
	#return HttpResponse(ordinary)
	
class cpf:

	def __init__(self,request):
		self.ordinary = number(request,'ordinary')
		self.special = number(request,'special')
		self.medisave = number(request,'medisave')
		self.medishield = number(request,'medishield')
		self.dps = number(request,'dps')
		self.date = get_date(request)
		self.jrnl = jrnl = 'cpf' + str(randint(0,99999))
		self.ref = 'CPF-0' + str(get_month(get_date(request))) + str(get_year(get_date(request)))
		

def number(request,item):
	n = request.POST.get(item,'')
	if n is None or n == '':
		n = 0
	n = float(n)
	return n
	
def get_month(date):
	return datetime.strptime(date, '%Y-%m-%d').strftime('%b')
	
'''