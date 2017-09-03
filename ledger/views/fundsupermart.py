from datetime import datetime, timedelta
from random import randint
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms

from ledger.models import investment_info,investment_transaction,journal,ledger,cashflow,parameter
from django.contrib.auth.models import User

#############################################################
# name: fundsupermart_journal_form
# type: form
# import by: ledger/view/init
# use: HTML form for fundsupermart related transactions
#############################################################
# version author description                      date
# 1.0     awai   initial release                  18/12/2016
#############################################################

class fundsupermart_journal_form(forms.Form):
	vickers_activities = (
	('buy','buy'),
	('sell','sell'),
	('commission','commission'),
	)
	date = forms.DateField(initial=datetime.now().strftime("%Y-%m-%d"))
	choice =  forms.ChoiceField(choices = vickers_activities,label='activities')
	fund = forms.CharField(max_length=10)
	unit = forms.DecimalField(max_digits=10, decimal_places=2)
	amount = forms.DecimalField(max_digits=10, decimal_places=2)
	
##############################################################
# name: fundsupermart_handler
# type: function
# import by: ledger/urls
# use: main view module for fundsupermart related transactions
##############################################################
# version author description                      date
# 1.0     awai   initial release                  18/12/2016
# 1.1     awai   support for ajex                 25/12/2016
##############################################################

def fundsupermart_handler(request):
	if request.method == 'POST':
		#return HttpResponse("Hello world.")
		
		user = User.objects.get(username=request.user.username).first_name
		choice = request.POST.get('choice','')
		ticker = request.POST.get('fund','').upper()
		date = request.POST.get('date','')
		jrnl = 'fundsupermart' + str(randint(0,99999))
		
		error = ''
		
		i_info_1 = investment_info.get(ticker,user)
		i_info_pre = investment_info.get(ticker,user)
		
		sign = -1 if choice == 'sell' or choice == 'commission' else 1
		
		amount = abs(float(request.POST.get('amount','')))
	
		unit = abs(float(request.POST.get('unit','')))
		return HttpResponse(unit)
		total_unit = float(i_info_1.unit) + unit * sign
		
		#update source
		try:
			transaction_update(choice,ticker,date,amount,unit,total_unit,'SGD',jrnl,user)
		except:
			error = error + '\ninsert transaction error'
		#info_update(choice,i_info_1,amount,unit,total_unit,'SGD')
		#update journal
		#i_info_new = investment_info.get(ticker,user)
		#journal_update(i_info_pre,i_info_new,date,choice,jrnl,user)
		#ledger.post(jrnl)
			
		if error == '':
			return HttpResponse('success')
		else:
			return HttpResponse(error)
	else:
		return HttpResponseRedirect(reverse('ledger:journals'))
		
def transaction_update(ac,ticker,date,amount,unit,total_unit,currency,jrnl,user):
	a1 = amount if ac == 'sell' else - amount
	price = amount / unit                         #value of transaction,
	a2 = total_unit * price                       #value of total shares, for simulation
	mode = parameter.mode()
	
	#clear previous sell simulation
	investment_transaction.clear_simulation(ticker,user,mode)
	#add actual transaction
	investment_transaction.add(date,ticker,'actual',ac,unit,price,a1,currency,jrnl,user,mode)
	#add new sell simulation
	investment_transaction.add(date,ticker,'simulating','sell',total_unit,price,a2,currency,jrnl,user,mode)
	
def info_update(ac,i_info_1,amount,unit,total_unit,currency):
	
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
	
def journal_update(i_info_1,i_info_2,date,choice,jrnl,user):
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