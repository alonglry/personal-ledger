from ..models import cashflow
from django.db.models import F
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect

def add_cashflow(date,choice,amount):
	m = get_month(date)
	y = get_year(date)
	amt = abs(amount)
	ac = choice
	
	if ac == '4G':
		ac = 'phone'
	elif ac == 'Citi dividend':
		ac = 'dividendcard'
	
	try:
		cashflow.objects.update_or_create(year = y, month = m, defaults = {ac:amt})
	except:
		if ac == 'salary':
			cashflow(year = y, month = m, salary = amt).save()
		elif ac == 'rental':
			cashflow(year = y, month = m, rental = amt).save()
		elif ac == 'phone':
			cashflow(year = y, month = m, phone = amt).save()
		elif ac == 'dividendcard':
			cashflow(year = y, month = m, dividendcard = amt).save()
	
	c = cashflow.objects.get(year = y, month = m)
	c.saving = t(c.salary) - t(c.rental) - t(c.phone) - t(c.dividendcard)
	c.save()
	
	#return HttpResponse('t')
	
def get_year(date):
	m = get_month(date)
	y =	int(datetime.strptime(date, '%Y-%m-%d').strftime('%Y'))
	if m == 12:
		y = y - 1
	return y

def get_month(date):
	m = int(datetime.strptime(date, '%Y-%m-%d').strftime('%m')) - 1
	if m == 0:
		m = 12
	return m
	
def t(n):
	if n is None:
		t = 0
	else:
		t = n
	return t