import datetime
from random import randint
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django import forms	

from ..models import investment_info,investment_transaction,journal,ledger,parameter,cashflow
from django.contrib.auth.models import User
from ledger.utils import user_name, device

#############################################################
# name: dbs_sos_journal_form
# type: form
# import by: ledger/view/init
# use: HTML form for DBS SOS related transactions
#############################################################
# version author description                      date
# 1.0     awai   initial release                  27/12/2016
#############################################################

class dbs_sos_journal_form(forms.Form):
	dbs_sos_activities = (
	('buy','buy'),
	('sell','sell'),
	('dividend','dividend'),
	)
	date = forms.DateField(initial=datetime.datetime.now().strftime("%Y-%m-%d"))
	choice =  forms.ChoiceField(choices = dbs_sos_activities,label='activities')
	unit = forms.DecimalField(max_digits=10, decimal_places=2,required = False)
	amount = forms.DecimalField(initial=615, max_digits=10, decimal_places=2,required = False)
	
##############################################################
# name: sos_handler
# type: function
# import by: ledger/urls
# use: main view module for DBS SOS related transactions
##############################################################
# version author description                      date
# 1.0     awai   initial release                  27/12/2016
# 1.1     awai   add test mode                    01/01/2017
# 1.2     awai   bug fix                          30/01/2017
#                decommission jounral             
##############################################################

def sos_handler(request):
	
	try:
		d = device(request)
	except Exception as err:
		return render(request,'ledger/error_page.html',{'device':'phone','message':err.args[0]})	

	try:
		user = user_name(request)
	except Exception as err:
		return render(request,'ledger/error_page.html',{'device':d,'message':err.args[0]})
	
	if request.method == 'POST':
		
		error = ''
		
		#get variables
		try:
			choice = request.POST.get('choice','')
			date = request.POST.get('date','')
			jrnl = 'SOS' + str(randint(0,99999))
			sign = -1 if choice == 'sell' or choice == 'dividend' else 1
		except:
			error = error + '\nget variables error'
			
		try:		
			ii = investment_info.objects.get(identifier='SOS',owner=user)
			#i_info_pre = investment_info.objects.get(identifier='SOS',owner=user)
		except:
			error = error + '\nget investment_info error'
			
		try:
			it = investment_transaction.objects.filter(investment_info = ii)
		except:
			error = error = '\nget investment_transaction error'
		
		if choice == 'buy' or choice == 'sell':
			amount = abs(float(request.POST.get('amount','')))
			unit = abs(float(request.POST.get('unit','')))
			total_unit = float(ii.unit) + unit * sign
		elif choice == 'dividend':
			amount = abs(float(request.POST.get('amount','')))
			unit = float(ii.unit)
			total_unit = float(ii.unit)
				
		#update source
		try:
			transaction_update(ii,it,choice,'SOS',date,amount,unit,total_unit,'SGD',jrnl,user)
		except:
			error = error + '\ninsert investment_transaction error'
		#error = error + info_update(choice,'SOS',user,amount,unit,'SGD')
		
		'''
		#update journal
		try:
			i_info_new = investment_info.get_shares_info(ticker,user)
			journal_update(i_info_pre,i_info_new,date,choice,jrnl,user)
		except:
			error = error + '\ninsert journal error'
		
		try:
			ledger.post(jrnl)
		except:
			error = error + '\nupdate ledger error'
		'''	
		if error == '':
			return HttpResponse('success')
		else:
			return HttpResponse(error)
		
	else:
		return HttpResponseRedirect(reverse('ledger:journals'))
		
def transaction_update(ii,it,ac,ticker,date,amount,unit,total_unit,currency,jrnl,user):
	error = ''
	
	#get variables
	try:
		price = round(amount / unit,5)
		mode = parameter.mode()
		
		if ac == 'buy':
			#self paid money transaction
			a1 = - round(amount * 2 / 3,5)
			u1 = round(unit * 2 / 3,5)
			p1 = abs(price)
			#company compensation
			a2 = round(amount / 3,5)
			u2 = round(unit / 3,5)
			p2 = abs(price)
			#simulation
			a3 = total_unit * price
			u3 = total_unit
			p3 = abs(price)		
		elif ac == 'sell':
			#actual
			u1 = unit
			p1 = abs(price)
			a1 = amount
			#simulation
			u2 = total_unit
			a2 = u2 * price
			p2 = abs(price)
		elif ac == 'dividend':
			#actual
			u1 = unit
			p1 = abs(price)
			a1 = amount
	except:
		error = error + '\ninsert transaction: get variables error'
	
	#insert investment transaction
	try:
		if ac == 'buy':
			#clear previous sell simulation
			if mode == 'test':
				it.filter(transaction_type_1 = 'simulating').exclude(mode=mode).transaction_type_1 = 'simulating_test'
				it.filter(transaction_type_1 = 'simulating',mode = 'test').delete()
			else:
				it.filter(transaction_type_1 = 'simulating').delete()
			#add actual transaction -- self paid money
			investment_transaction.objects.create(date = date,investment_info = ii,transaction_type_1 = 'actual',transaction_type_2 = 'buy',unit = u1,price = p1,amount = a1,currency = 'SGD',mode = mode,broker_company = 'DBS',account = 'SOS')
			#add actual transaction -- company compensation
			investment_transaction.objects.create(date = date,investment_info = ii,transaction_type_1 = 'actual',transaction_type_2 = 'compensation',unit = u2,price = p2,amount = a2,currency = 'SGD',mode = mode,broker_company = 'DBS',account = 'SOS')
			#add new sell simulation
			investment_transaction.objects.create(date = date,investment_info = ii,transaction_type_1 = 'simulating',transaction_type_2 = 'sell',unit = u3,price = p3,amount = a3,currency = 'SGD',mode = mode,broker_company = 'DBS',account = 'SOS')
		elif ac == 'sell':
			#clear previous sell simulation
			investment_transaction.clear_simulation(ticker,user,mode)
			#add actual transaction
			investment_transaction.add(date,ticker,'actual',ac,u1,p1,a1,currency,jrnl,user,mode,'DBS','SOS')
			#add new sell simulation -- unsold shares
			investment_transaction.add(date,ticker,'simulating','sell',u2,p2,a2,currency,jrnl,user,mode,'DBS','SOS')
		elif ac == 'dividend':
			#add actual transaction
			investment_transaction.objects.create(date = date,investment_info = ii,transaction_type_1 = 'actual',transaction_type_2 = 'dividend',unit = u1,price = p1,amount = a1,currency = 'SGD',mode = mode,broker_company = 'DBS',account = 'SOS')
	except:
		error = error + '\ninsert transaction: insert investment transaction error'
		
	return error
			
	
def info_update(ac,ticker,user,amount,unit,currency):
	error = ''
	
	#get variables
	try:
		mode = parameter.mode()
		info = investment_info.get_shares_info(ticker,user)
		sign = -1 if ac == 'sell' or ac == 'dividend' else 1
		price = amount / unit
	except:
		error = error + '\nupdate investment info: get variables error'
		
	#save non-static columns into remark
	try:
		if mode == 'test' and info.remark == None:
			info.remark = info.dict_test_mode
			info.save()
	except:
		error = error + '\nupdate investment info: prepare test mode error'
		
	#update account info
	try:
		
		if ac == 'buy' or ac == 'sell':
						
			info.unit 				 = float(info.unit) + sign * unit 
			info.last_update_amount  = float(info.last_update_amount) + sign * amount
			info.current_price 		 = price
			#info.current_amount		 = info.unit * info.current_price
			info.currency 			 = currency
			
			if ac == 'buy':
				info.paid_amount     = float(info.paid_amount) + abs(amount * 2 / 3)
			elif ac == 'sell':
				info.sold_amount     = float(info.sold_amount) + abs(amount)
			
			#info.profit_loss         = info.current_amount - float(info.paid_amount) + float(info.sold_amount)
			#info.total_profit_loss   = float(info.profit_loss) + float(info.dividend)
			
		elif ac == 'dividend':
			info.dividend            = float(info.dividend) + amount
			#info.total_profit_loss   = float(info.total_profit_loss) + info.dividend
					
		info.save()
		
	except:
		error = error + '\nupdate investment info: update investment info error'
		
	return error
	
	
def journal_update(i_info_1,i_info_2,date,choice,jrnl,user):
	error = ''
	
	mode = parameter.mode()
	
	if choice == 'buy':
		#get variables
		try:
			s = float(i_info_2.last_update_amount) - float(i_info_1.last_update_amount)
			u = round(abs(float(i_info_2.unit) - float(i_info_1.unit)),2)
			p = round(float(i_info_2.current_price),2)
			
			upl = (float(i_info_2.profit_loss) - float(i_info_1.profit_loss)) - ((float(i_info_2.paid_amount) - float(i_info_1.paid_amount)) / 2)
			cu = 'SGD'
			
			acg = 'SG shares'
			ac = 'SOS'
			
			#shares
			gl_1 = a_1 = 'DBS SOS'
			gl_2 = 'salary' + ' ' + str(get_year(date))
			a_2 = None
			ref = 'SOS' + '-' + str(get_prev_month(date)) + ' ' + str(get_year(date))
			journal.add(date,s,cu,'asset',ac,acg,ref,a_1,gl_1,jrnl,user,mode)
			journal.add(date,-s,cu,'income',ac,acg,ref,a_2,gl_2,jrnl,user,mode)
			
			#UPL
			gl_1 = 'shares UPL'
			a_1 = None
			gl_2 = a_2 = 'DBS SOS'
			ref = 'mtm' + '-' + 'SOS' +'-('+str(round(float(i_info_1.current_price),2))+','+str(p)+')-'+str(float(i_info_1.unit))
		except:
			error = error + '\ninsert journal: get variables error'
		
		#insert journal
		try:
			journal.add(date,-upl,cu,'income',ac,acg,ref,a_1,gl_1,jrnl,user,mode)
			journal.add(date,upl,cu,'asset',ac,acg,ref,a_2,gl_2,jrnl,user,mode)
		except:
			error = error + '\ninsert journal: insert journal error'
	elif choice == 'dividend':
		gl_1 = a_1 = 'POSB savings'
		gl_2 = 'shares dividend'
		a_2 = None
		cu = 'SGD'
		ac = 'SOS'
		acg = 'SG shares'
		
		amt = float(i_info_2.dividend) - float(i_info_1.dividend)
		unit = float(i_info_2.unit)
		price = round(amt/unit,2)
		
		ref = 'dividend-SOS-(' + str(price) + ',' + str(unit) + ')'
		
		journal.add(date,-amt,cu,'income',ac,acg,ref,a_2,gl_2,jrnl,user,mode)
		journal.add(date,amt,cu,'asset',ac,acg,ref,a_1,gl_1,jrnl,user,mode)
		
	
def get_month(date):
	return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%b')
	
def get_year(date):
	return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y')
	
def get_prev_month(date):
	return (datetime.datetime.strptime(date, '%Y-%m-%d').replace(day=1) - datetime.timedelta(days=1)).strftime('%b')