'''
from datetime import datetime
from random import randint

from ..utils.ledger import get_date, journal_add, journal_post, get_year
from ..utils.investment import investment_transaction_clear_simulation, investment_transaction_add, commission, get_shares_info, all_investments

def SOS_handler(request):
	choice = request.POST.get('choice','')
	ticker = 'SOS'
	date = get_date(request)
	jrnl = 'SOS' + str(randint(0,99999))
	
	i_info_1 = get_shares_info(ticker)
	i_info_pre = get_shares_info(ticker)
	
	sign = -1 if choice == 'sell' or choice == 'dividend' else 1
	
	if choice == 'buy' or choice == 'sell':
		amount = abs(float(request.POST.get('amount','')))
		unit = abs(float(request.POST.get('unit','')))
		total_unit = float(i_info_1.unit) + unit * sign
		
		
	if choice == 'buy' or choice == 'sell':
		#update source
		investment_transaction_update(choice,ticker,date,amount,unit,total_unit,'SGD',jrnl)
		investment_info_update(choice,i_info_1,amount,unit,total_unit,'SGD')
		#update journal
		i_info_new = get_shares_info(ticker)
		journal_update(i_info_pre,i_info_new,date,choice,jrnl)
		journal_post(jrnl)
		
def investment_transaction_update(ac,ticker,date,amount,unit,total_unit,currency,jrnl):
	price = round(amount / unit,2)
	
	if ac == 'buy':
		a1 = - round(amount * 2 / 3,2)
	elif ac == 'sell':
		a1 = amount
		
	a2 = total_unit * price
	
	investment_transaction_clear_simulation(ticker)
	investment_transaction_add(date,ticker,'actual',ac,unit,abs(round(a1 / unit,2)),a1,currency,jrnl)
	if ac == 'buy':
		investment_transaction_add(date,ticker,'actual','compensation',unit,abs(round(a1 / 2 / unit,2)),round(-a1 / 2,2),currency,jrnl)
	investment_transaction_add(date,ticker,'simulating','sell',total_unit,price,a2,currency,jrnl)
	
def investment_info_update(ac,i_info_1,amount,unit,total_unit,currency):
	price = round(amount / unit,2)
	
	if ac == 'buy':
		a1 = round(amount * 2 / 3,2)
		a = amount
	elif ac == 'sell':
		a1 = - amount
		a = - amount
		
	a2 = total_unit * price
	
	d = round(amount / 3,2)
	
	i_info_1.unit               = total_unit
	i_info_1.last_update_amount = float(i_info_1.last_update_amount) + a
	i_info_1.current_price      = price
	i_info_1.current_amount     = a2
	i_info_1.currency           = currency
	
	if ac == 'buy':
		pa                      = float(i_info_1.paid_amount) + abs(a1) #paid amount for total shares
		i_info_1.paid_amount    = pa
		i_info_1.profit_loss    = a2 - pa
	elif ac == 'sell':
		sa                      = float(i_info_1.sold_amount) + abs(a1) #sold amount for total shares
		i_info_1.sold_amount    = sa
		i_info_1.profit_loss    = a2 + sa
		
	i_info_1.total_profit_loss  = float(i_info_1.profit_loss)
		
	i_info_1.save()
	
def journal_update(i_info_1,i_info_2,date,choice,jrnl):
	s = float(i_info_2.last_update_amount) - float(i_info_1.last_update_amount)
	u = round(abs(float(i_info_2.unit) - float(i_info_1.unit)),2)
	p = round(float(i_info_2.current_price),2)
	
	upl = (float(i_info_2.profit_loss) - float(i_info_1.profit_loss)) - ((float(i_info_2.paid_amount) - float(i_info_1.paid_amount)) / 2)
	cu = 'SGD'
	
	acg = 'SG shares'
	ac = 'SOS'
	
	#shares
	gl_1 = a_1 = 'DBS SOS'
	gl_2 = a_2 = 'salary' + ' ' + str(get_year(date))
	ref = 'SOS' + '-' + str(get_month(date)) + ' ' + str(get_year(date))
	
	journal_add(date,s,cu,'asset',ac,acg,ref,a_1,gl_1,jrnl)
	journal_add(date,-s,cu,'income',ac,acg,ref,a_2,gl_2,jrnl)
	
	#UPL
	gl_1 = 'shares UPL'
	a_1 = None
	gl_2 = a_2 = 'DBS SOS'
	ref = 'mtm' + '-' + 'SOS' +'-('+str(round(float(i_info_1.current_price),2))+','+str(p)+')-'+str(float(i_info_1.unit))
	journal_add(date,-upl,cu,'income',ac,acg,ref,a_1,gl_1,jrnl)
	journal_add(date,upl,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl)
	
def get_month(date):
	return datetime.strptime(date, '%Y-%m-%d').strftime('%b')
'''