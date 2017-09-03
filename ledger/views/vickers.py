from datetime import datetime, timedelta
from random import randint
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from ledger.models import cashflow,journal,ledger,investment_info,account_info

from ..forms import vickers_journal_form

def vickers_handler(request):
	if request.method == 'POST':
		#return HttpResponse("Hello, world. cpf")
		
		if vickers_journal_form(request.POST).is_valid():
			user = request.user.username
			choice = request.POST.get('choice','')
			ticker = request.POST.get('ticker','').upper()
			date = request.POST.get('date','')
			jrnl = 'vickers' + str(randint(0,99999))
			price = float(request.POST.get('price','0')) if request.POST.get('price','0') <> '' else 0
			unit = float(request.POST.get('unit','0')) if request.POST.get('unit','0') <> '' else 0
			
			sign = -1 if choice == 'sell' or choice == 'dividend' else 1
			
			if choice == 'buy' or choice == 'sell':
				i_info_1 = investment_info.get(ticker,user)
				i_info_pre = investment_info.get(ticker,user)
				i_info_new = investment_info.get(ticker,user)
				price = abs(float(request.POST.get('price','')))
				unit = abs(float(request.POST.get('unit','')))
				total_unit = float(i_info_1.unit) + unit * sign
			elif choice == 'dividend':
				i_info_1 = investment_info.get(ticker,user)
				i_info_pre = investment_info.get(ticker,user)
				i_info_new = investment_info.get(ticker,user)
				total_unit = float(i_info_1.unit)
				unit = total_unit
				price = abs(float(request.POST.get('price',''))) / total_unit
			elif choice == 'transfer':
				unit = 0
				total_unit = 0
				i_info_1 = None
				i_info_pre = None
				i_info_new = None
				
			if price <> 0:
				#update source
				transaction_update(choice,ticker,date,price,unit,total_unit,'SGD',jrnl,user)
				info_update(choice,i_info_1,price,unit,total_unit,'SGD',user)
				#update journal
				journal_update(i_info_pre,i_info_new,date,choice,jrnl,user,price)
				ledger.post(jrnl)
			
			return HttpResponseRedirect(reverse('ledger:journals'))
		else:
			return HttpResponseRedirect(reverse('ledger:journals'))
	else:
		return HttpResponseRedirect(reverse('ledger:journals'))
		
def transaction_update(choice,ticker,date,amount,unit,total_unit,currency,jrnl,user):
	if choice == 'transfer':
		cashflow.add(date,'vickers','deposit','deposit',user,amount,'SGD',jrnl)
		cashflow.add(date,'POSB','savings','investment',user,-amount,'SGD',jrnl)
	
def info_update(ac,i_info_1,amount,unit,total_unit,currency,user):
	
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
		
		i_info_1.save()
			
	elif ac == 'commission':
		a2 = float(i_info_1.current_price) * total_unit
		c2 = float(i_info_1.commission) + amount
		
		i_info_1.unit               = total_unit
		i_info_1.current_amount     = a2
		i_info_1.commission         = c2
		
		i_info_1.total_profit_loss  = float(i_info_1.profit_loss) - c2
		
		i_info_1.save()
		
	elif ac == 'transfer':
		account_info.update('vickers','deposit',user,amount)
		account_info.update('POSB','savings',user,-amount)
	
def journal_update(i_info_1,i_info_2,date,choice,jrnl,user,amount=None):
	if choice <> 'transfer':
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
		journal.add(date,s,cu,'asset',ac,acg,ref,a_1,gl_1,jrnl,user)
		journal.add(date,-s,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl,user)
		
		#commission
		gl_1 = 'funds commission'
		a_1 = None
		gl_2 = a_2 = 'fundsupermart'
		ref = choice + '-' + i_info_2.identifier +'-'+str(p)+'-'+str(u)
		journal.add(date,c,cu,'expense',ac,acg,ref,a_1,gl_1,jrnl,user)
		journal.add(date,-c,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl,user)
		
		#UPL
		gl_1 = 'funds UPL'
		a_1 = None
		gl_2 = a_2 = 'fundsupermart'
		ref = 'mtm' + '-' + i_info_2.identifier +'-('+str(round(float(i_info_1.current_price),2))+','+str(p)+')-'+str(float(i_info_1.unit))
		journal.add(date,-upl,cu,'income',ac,acg,ref,a_1,gl_1,jrnl,user)
		journal.add(date,upl,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl,user)
	
	else:
		gl_2 = a_2 = 'POSB savings'
		gl_1 = a_1 = 'vickers deposit'
		ref = 'tansfer-vickers-'+(str(amount) if amount >= 0 else '(' + str(abs(amount)) + ')')
		ac = 'vickers deposit' if amount >= 0 else 'vickers withdraw'
		acg = 'cash'
		
		journal.add(date,amount,'SGD','asset',ac,acg,ref,a_1,gl_1,jrnl,user,'vickers')
		journal.add(date,-amount,'SGD','asset',ac,acg,ref,a_2,gl_2,jrnl,user,'vickers')