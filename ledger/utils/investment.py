from ..models import investment_transaction, investment_info


def investment_transaction_clear_simulation(ticker):
	try:
		investment_transaction.objects.filter(identifier_id=ticker,transaction_type_1='simulating').delete()
	except:
		pass

def investment_transaction_add(d,i,t1,t2,u,p,a,c,j):
	investment_transaction(date = d,
		          identifier_id = i,
	         transaction_type_1 = t1,
		     transaction_type_2 = t2,
						   unit = u,
						  price = p,
						 amount = a,
				       currency = c,
					 journal_id = j).save()
					   
def commission(a,t):
	if t == 'vickers':
		return round(max(13.17,abs(a) * 0.0028),2)
	else:
		return 0
		
def get_shares_info(ticker):
	info = investment_info.objects.get_or_create(identifier=ticker,defaults={'country':country(ticker)})
	info = investment_info.objects.get(identifier=ticker)
	
	return info	

def get_funds_info(ticker):
	info = investment_info.objects.get_or_create(identifier=ticker,defaults={'type':'funds','country':country(ticker)})
	info = investment_info.objects.get(identifier=ticker,type='funds')
	
	return info
	
def all_investments():
	return investment_info.objects.order_by().values_list('identifier','current_amount').distinct().exclude(identifier = '')
	#return investement_info.objects.all()
	
def investment_percentage(ticker,amount,total_amount):
	i = investment_info.objects.get(identifier=ticker)
	i.percentage = amount / total_amount * 100
	i.save()
	
def country(ticker):
	if ticker[-3:].upper() == '.SI':
		return 'SG'
	else:
		return 'others'
		
'''
def fvalue (cashflow,x,prime):
	result = 0
	days = 0
	
	for c in cashflow:
'''	