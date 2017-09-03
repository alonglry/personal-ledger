'''from django.http import HttpResponse, HttpResponseRedirect
from random import randint

from ..utils.investment import investment_transaction_clear_simulation, investment_transaction_add, commission, get_funds_info, all_investments, investment_percentage
from ..utils.ledger import get_date, journal_add, journal_post

def fundsupermart_handler(request):
	choice = request.POST.get('choice','')
	ticker = request.POST.get('fund','').upper()
	date = get_date(request)
	jrnl = 'fundsupermart' + str(randint(0,99999))
	
	i_info_1 = get_funds_info(ticker)
	i_info_pre = get_funds_info(ticker)
	
	sign = -1 if choice == 'sell' or choice == 'commission' else 1
	
	amount = abs(float(request.POST.get('amount','')))
	
	unit = abs(float(request.POST.get('unit','')))
	price = amount / unit
	total_unit = float(i_info_1.unit) + unit * sign
	
	#update source
	investment_transaction_update(choice,ticker,date,amount,unit,total_unit,sign,'SGD',jrnl)
	investment_info_update(choice,i_info_1,amount,unit,total_unit,sign,'SGD')
	#update journal
	i_info_new = get_funds_info(ticker)
	journal_update(i_info_pre,i_info_new,date,choice,jrnl)
	journal_post(jrnl)
	#return HttpResponse('nhtnn')
	
def investment_transaction_update(ac,ticker,date,amount,unit,total_unit,sign,currency,jrnl):
	a1 = - amount * sign
	price = amount / unit                         #value of transaction,
	a2 = total_unit * price                       #value of total shares, for simulation
	
	investment_transaction_clear_simulation(ticker)
	investment_transaction_add(date,ticker,'actual',ac,unit,price,a1,currency,jrnl)
	investment_transaction_add(date,ticker,'simulating','sell',total_unit,price,a2,currency,jrnl)
	
def investment_info_update(ac,i_info_1,amount,unit,total_unit,sign,currency):
	
	if ac == 'buy' or ac == 'sell':
		a1 = amount                                    #value of transaction
		price = amount / unit
		a2 = total_unit * price                        #value of total shares
		
		i_info_1.unit               = total_unit
		i_info_1.last_update_amount = float(i_info_1.last_update_amount) + a1
		i_info_1.current_price      = price
		i_info_1.current_amount     = a2
		i_info_1.currency           = currency
		
		if ac == 'buy':
			pa                      = float(i_info_1.paid_amount) + a1 #paid amount for total shares
			i_info_1.paid_amount    = pa
			i_info_1.profit_loss    = a2 - pa
		elif ac == 'sell':
			sa                      = float(i_info_1.sold_amount) + a1 #sold amount for total shares
			i_info_1.sold_amount    = sa
			i_info_1.profit_loss    = a2 + sa
			
		i_info_1.total_profit_loss  = float(i_info_1.profit_loss) - float(i_info_1.commission)
			
	elif ac == 'commission':
		a2 = float(i_info_1.current_price) * total_unit
		c2 = float(i_info_1.commission) + amount
		
		i_info_1.unit               = total_unit
		i_info_1.current_amount     = a2
		i_info_1.commission         = c2
		
		i_info_1.total_profit_loss  = float(i_info_1.profit_loss) - c2
		
	i_info_1.save()
	
def journal_update(i_info_1,i_info_2,date,choice,jrnl):
	s = float(i_info_2.last_update_amount) - float(i_info_1.last_update_amount)
	u = abs(float(i_info_2.unit) - float(i_info_1.unit))
	#p = abs(round(s / u,2))
	p = round(float(i_info_2.current_price),2)
	u = round(u,2)
	
	upl = float(i_info_2.profit_loss) - float(i_info_1.profit_loss)
	c = float(i_info_2.commission) - float(i_info_1.commission)
	d = float(i_info_2.dividend) - float(i_info_1.dividend)
	cu = i_info_2.currency
	
	i = i_info_2.identifier
	acg = i_info_2.country + ' ' + i_info_2.type
	ac = i_info_2.identifier
	
	#shares
	gl_1 = a_1 = 'fundsupermart'
	gl_2 = a_2 = 'POSB savings'
	ref = choice + '-' + i_info_2.identifier +'-'+str(p)+'-'+str(u)
	journal_add(date,s,cu,'asset',ac,acg,ref,a_1,gl_1,jrnl)
	journal_add(date,-s,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl)
	
	#commission
	gl_1 = 'funds commission'
	a_1 = None
	gl_2 = a_2 = 'fundsupermart'
	ref = choice + '-' + i_info_2.identifier +'-'+str(p)+'-'+str(u)
	journal_add(date,c,cu,'expense',ac,acg,ref,a_1,gl_1,jrnl)
	journal_add(date,-c,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl)
	
	#UPL
	gl_1 = 'funds UPL'
	a_1 = None
	gl_2 = a_2 = 'fundsupermart'
	ref = 'mtm' + '-' + i_info_2.identifier +'-('+str(round(float(i_info_1.current_price),2))+','+str(p)+')-'+str(float(i_info_1.unit))
	journal_add(date,-upl,cu,'income',ac,acg,ref,a_1,gl_1,jrnl)
	journal_add(date,upl,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl)
'''