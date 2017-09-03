'''from django.http import HttpResponse, HttpResponseRedirect
#from django.core.urlresolvers import reverse
from datetime import datetime,timedelta
#from django.db.models import F
from random import randint

from ..utils.investment import investment_transaction_clear_simulation, investment_transaction_add, commission, get_shares_info, all_investments, investment_percentage
from ..utils.ledger import get_date, journal_add, journal_post
from ..utils.stock import get_price, t

def vickers_mtm_handler(request):
	ta = 0 #total amount of all investments
	all = all_investments()
	
	#mark to market for every share
	for a in all:
		ticker = a[0]
		price = get_price(ticker)
		date = get_date(request)
		ta = ta + a[1]
		
		if price <> 0:
			
			i_info_1 = get_shares_info(t(ticker))
			i_info_pre = get_shares_info(t(ticker))
			jrnl = 'vickers' + str(randint(0,99999))
			
			total_unit = unit = float(i_info_1.unit)
			sign = 1
			
			#update source
			investment_transaction_mtm(t(ticker),date,price,total_unit,'SGD',jrnl)
			investment_info_update('mtm',i_info_1,price,unit,total_unit,sign,'SGD')
			#update journal
			i_info_new = get_shares_info(t(ticker))
			journal_update(i_info_pre,i_info_new,date,'mtm',jrnl)
			#update ledger
			journal_post(jrnl)
	
	#calculate precentage for every share
	for a in all:
		#return HttpResponse(ta)
		investment_percentage(a[0],a[1],ta)
	
def vickers_handler(request):
	choice = request.POST.get('choice','')
	ticker = request.POST.get('ticker','').upper()
	date = get_date(request)
	jrnl = 'vickers' + str(randint(0,99999))
	
	i_info_1 = get_shares_info(ticker)
	i_info_pre = get_shares_info(ticker)
	
	sign = -1 if choice == 'sell' or choice == 'dividend' else 1
	
	if choice == 'buy' or choice == 'sell':
		price = abs(float(request.POST.get('price','')))
		unit = abs(float(request.POST.get('unit','')))
		total_unit = float(i_info_1.unit) + unit * sign
	elif choice == 'dividend':
		total_unit = float(i_info_1.unit)
		unit = total_unit
		price = abs(float(request.POST.get('price',''))) / total_unit
	elif choice == 'transfer':
		amt = float(request.POST.get('price',''))
		gl_2 = a_2 = 'POSB savings'
		gl_1 = a_1 = 'vickers deposit'
		ref = 'tansfer-vickers-'+(str(amt) if amt >= 0 else '(' + str(abs(amt)) + ')')
		ac = 'vickers deposit' if amt >= 0 else 'vickers withdraw'
		
	if choice == 'buy' or choice == 'sell':
		#update source
		investment_transaction_update(choice,ticker,date,price,unit,total_unit,sign,'SGD',jrnl)
		investment_info_update(choice,i_info_1,price,unit,total_unit,sign,'SGD')
		#update journal
		i_info_new = get_shares_info(ticker)
		journal_update(i_info_pre,i_info_new,date,choice,jrnl)
		journal_post(jrnl)
	elif choice == 'transfer':
		#update journal
		journal_add(date,amt,'SGD','asset',ac,None,ref,a_1,gl_1,jrnl)
		journal_add(date,-amt,'SGD','asset',ac,None,ref,a_2,gl_2,jrnl)
		journal_post(jrnl)
	elif choice == 'dividend':
		#update source
		investment_transaction_update(choice,ticker,date,price,unit,total_unit,sign,'SGD',jrnl)
		investment_info_update(choice,i_info_1,price,unit,total_unit,sign,'SGD')
		i_info_new = get_shares_info(ticker)
		journal_update(i_info_pre,i_info_new,date,choice,jrnl)
		journal_post(jrnl)
	#return HttpResponse('nnn')
	
#private functions
def investment_transaction_mtm(ticker,date,price,total_unit,currency,jrnl):
	a2 = total_unit * price                        #value of total shares, for simulation
	c2 = -commission(total_unit * price,'vickers') #value of commission for total shares, for simulation
	cp2 = abs(c2 / total_unit)                     #price of commission for total shares, for simulation
	
	investment_transaction_clear_simulation(ticker)
	investment_transaction_add(date,ticker,'simulating','commission',total_unit,cp2,c2,currency,jrnl)
	investment_transaction_add(date,ticker,'simulating','sell',total_unit,price,a2,currency,jrnl)

def investment_transaction_update(ac,ticker,date,price,unit,total_unit,sign,currency,jrnl):
	a1 = -sign * unit * price                      #value of transaction
	a2 = total_unit * price                        #value of total shares, for simulation
	c1 = -commission(a1,'vickers')                 #value of commission for this transaction
	cp1 = abs(c1 / unit)						   #price of commission per share for this transaction
	c2 = -commission(total_unit * price,'vickers') #value of commission for total shares, for simulation
	cp2 = abs(c2 / total_unit)                     #price of commission for total shares, for simulation
	
	investment_transaction_clear_simulation(ticker)
	investment_transaction_add(date,ticker,'actual',ac,unit,price,a1,currency,jrnl)
	
	if ac == 'buy' or ac == 'sell':
		investment_transaction_add(date,ticker,'actual','commission',unit,cp1,c1,currency,jrnl)		
	
	investment_transaction_add(date,ticker,'simulating','commission',total_unit,cp2,c2,currency,jrnl)
	investment_transaction_add(date,ticker,'simulating','sell',total_unit,price,a2,currency,jrnl)
	
def investment_info_update(ac,i_info_1,price,unit,total_unit,sign,currency):
	a1 = sign * unit * price                                    #value of transaction
	a2 = total_unit * price                                     #value of total shares	
	c2 = float(i_info_1.commission) + commission(a1,'vickers')  #value of commission for total shares, for simulation
	
	if ac == 'buy' or ac == 'sell':
		i_info_1.unit               = total_unit
		i_info_1.last_update_amount = float(i_info_1.last_update_amount) + a1
		i_info_1.current_price      = price
		i_info_1.current_amount     = a2		
		i_info_1.commission         = c2
		i_info_1.currency           = currency
		if ac == 'buy':
			pa                      = float(i_info_1.paid_amount) + abs(a1) #paid amount for total shares
			i_info_1.paid_amount    = pa
			i_info_1.profit_loss    = a2 - pa
		elif ac == 'sell':
			sa                      = float(i_info_1.sold_amount) + abs(a1) #sold amount for total shares
			i_info_1.sold_amount    = sa
			i_info_1.profit_loss    = a2 + sa
		i_info_1.total_profit_loss  = float(i_info_1.profit_loss) - c2
			
	elif ac == 'dividend':
		i_info_1.dividend           = float(i_info_1.dividend) + abs(a1)
		i_info_1.total_profit_loss  = float(i_info_1.total_profit_loss) + abs(a1)
		
	elif ac == 'mtm':
		i_info_1.current_price      = price
		i_info_1.current_amount     = a2
		pa                          = float(i_info_1.paid_amount) 
		sa                          = float(i_info_1.sold_amount)
		da                          = float(i_info_1.dividend)
		ca                          = float(i_info_1.commission)
		i_info_1.profit_loss        = a2 - pa + sa
		i_info_1.total_profit_loss  = a2 - pa + sa  + da - ca
		
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
	gl_1 = a_1 = 'CDP'
	gl_2 = a_2 = 'vickers deposit'
	ref = choice + '-' + i_info_2.identifier +'-'+str(p)+'-'+str(u)
	journal_add(date,s,cu,'asset',ac,acg,ref,a_1,gl_1,jrnl)
	journal_add(date,-s,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl)
	
	#commission
	gl_1 = 'shares commission'
	a_1 = None
	gl_2 = a_2 = 'vickers deposit'
	ref = choice + '-' + i_info_2.identifier +'-'+str(p)+'-'+str(u)
	journal_add(date,c,cu,'expense',ac,acg,ref,a_1,gl_1,jrnl)
	journal_add(date,-c,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl)
	
	#dividend
	gl_1 = 'shares dividend'
	a_1 = None
	gl_2 = a_2 = 'POSB savings'
	ref = choice + '-' + i_info_2.identifier +'-'+str(p)+'-'+str(u)
	journal_add(date,-d,cu,'income',ac,acg,ref,a_1,gl_1,jrnl)
	journal_add(date,d,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl)
	
	#UPL
	gl_1 = i_info_2.type + ' UPL'
	a_1 = None
	if i_info_2.type == 'shares':
		gl_2 = a_2 = 'CDP'
	elif i_info_2.type == 'funds':
		gl_2 = a_2 = 'fundsupermart'
		
	ref = 'mtm' + '-' + i_info_2.identifier +'-('+str(round(float(i_info_1.current_price),2))+','+str(p)+')-'+str(float(i_info_1.unit))
	journal_add(date,-upl,cu,'income',ac,acg,ref,a_1,gl_1,jrnl)
	journal_add(date,upl,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl)

		
def dateshift(date,shift):
	d = datetime.strptime(date,"%Y-%m-%d").date()
	s = timedelta(days=shift)
	return (d+s).strftime("%Y-%m-%d")
'''