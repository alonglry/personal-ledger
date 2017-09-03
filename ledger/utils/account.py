'''from ..models import account_info
from django.db.models import F

def account_balance_update(account,amount):
	account_info.objects.filter(identifier=account).update(amount=F('amount')+amount)

#single access to account_info model data
#used by: \user\personal_finance\ledger\views\accounts.py
#last update: 06/07/2016
#depreciated
def account_get(attr = ''):
	if attr == 'all':
		return account_info.objects.all()
	elif attr == 'meta':
		return account_info._meta
	elif attr == 'non-investment':
		return account_info.objects.exclude(type = 'shares').exclude(type='funds')
		
'''