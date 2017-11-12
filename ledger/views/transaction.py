from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

from ledger.models import cashflow,parameter
from ledger.utils import user_name, device
from ledger.forms import transaction_form

##############################################################
# name: transactions
# type: function
# import by: ledger/urls
#            ledger/views/_init_.py
# use: main view module for transaction (from source) page
##############################################################
# version author description                      date
# 1.0     awai   initial release                  23/07/2017
###############################################################

@login_required(login_url='/login/')
def transaction(request):
	
	try:
		d = device(request)
	except Exception as err:
		return render(request,'ledger/error_page.html',{'device':'phone','message':err.args[0]})	

	try:
		user = user_name(request)
	except Exception as err:
		return render(request,'ledger/error_page.html',{'device':d,'message':err.args[0]})
	
	if request.method <> 'POST':
		return render(request,'ledger/transaction.html',{'device':d,'textbox':transaction_form(),'user':user})

	else:
		error = ''
		
		try:
			id = request.POST.get('id','')
		except:
			error = error + '\nget action error'
			
		if id == 'upload':
		
			try:
				company = request.POST.get('company','')
			except:
				error = error + '\nget company error'
				
			try:
				text = request.POST.get('text','')
			except:
				error = error + '\nget text error'
			
			#POSB savings
			if text.strip() <> '' and company.strip() == 'POSB':
				line = text.splitlines()
				for l in line:
					word = l.split(",")
					if word[1] == 'NPW':
						cashflow.objects.update_or_create(
							date = datetime.strptime(word[0],'%d %b %Y'),
							detail = word[1] + '/' + word[5] + ' ' + word[6],
							year = datetime.strptime(word[0],'%d %b %Y').strftime('%Y'),
							month = datetime.strptime(word[0],'%d %b %Y').strftime('%m'),
							amount = float('-'+word[6].strip().split(' ')[1].strip()),
							company = 'POSB',
							owner = user,
							account = 'savings',
							currency = 'SGD',

							defaults={"mode": parameter.mode(),"item":'others'}
						)
						cashflow.objects.update_or_create(
							date = datetime.strptime(word[0],'%d %b %Y'),
							detail = word[1] + '/' + word[5] + ' ' + word[7],
							year = datetime.strptime(word[0],'%d %b %Y').strftime('%Y'),
							month = datetime.strptime(word[0],'%d %b %Y').strftime('%m'),
							amount = float('-'+word[7].strip().split(' ')[1].strip()),
							company = 'POSB',
							owner = user,
							account = 'savings',
							currency = 'SGD',

							defaults={"mode": parameter.mode(),"item":'cash'}
						)
					else:
						cashflow.objects.update_or_create(
							date = datetime.strptime(word[0],'%d %b %Y'),
							detail = word[1] + '/' + word[4] + '/' + word[5],
							year = datetime.strptime(word[0],'%d %b %Y').strftime('%Y'),
							month = datetime.strptime(word[0],'%d %b %Y').strftime('%m'),
							amount = float('-'+word[2].strip() if word[2].strip() <> '' else word[3]),
							company = 'POSB',
							owner = user,
							account = 'savings',
							currency = 'SGD',

							defaults={"mode": parameter.mode(),"item":word[7] if word[7] <> '' else dbs_get_item(word[1],word[4])}
						)
			#Citi dividend card
			elif text.strip() <> '' and company.strip() == 'Citi':
				line = text.splitlines()
				for l in line:
					word = l.split("\t")
					cashflow.objects.update_or_create(
						date = datetime.strptime(word[0],'%d/%m/%Y'),
						detail = word[1],
						year = datetime.strptime(word[0],'%d/%m/%Y').strftime('%Y'),
						month = datetime.strptime(word[0],'%d/%m/%Y').strftime('%m'),
						amount = float('-'+word[2].strip().split(' ')[1].strip().replace(',','') if word[2].strip() <> '' else word[3].strip().split(' ')[1].strip().replace(',','')),
						company = 'Citi',
						owner = user,
						account = 'Dividend Card',
						currency = 'SGD',

						defaults={"mode": parameter.mode(),"item":word[3] if (word[3] <> '' and word[3].find('SGD') <> 0) else citi_get_item(word[1])}
					)
			
				
		if error == '':
			return HttpResponse('success')
		else:
			return HttpResponse(error)
		
def dbs_get_item(code,ref):
	item = 'others'
	
	if code == 'PAY':
		item = 'salary'
	elif code == 'INT' or code == 'ADV':
		item = 'interest'
	elif code == 'AWL':
		item = 'cash'
	elif code == 'CDP' or ref.find('IFA -P0305995') <> -1:
		item = 'investment'
	elif ref.find('SPINELLI COFFEE') <> -1 or ref.find('96 BEVERAGE') <> -1 or ref.find('STARBUCKS') <> -1 or ref.find('CHILLIPADI') <> -1 or ref.find('SHENG KEE DESSERT') <> -1 or ref.find('BURGER KING') <> -1 or ref.find('MCDONALD') <> -1:
		item = 'F&B'
	elif code == 'ACT' or ref.find('COMFORT TRANSPORTATION') <> -1 or ref.find('PREMIER TAXIS') <> -1 or ref.find('SMRT TAXIS') <> -1 or ref.find('TRANS-CAB SERVICES') <> -1 or ref.find('FINANCE DEPT-IBG') <> -1:
		item = 'transport'
	elif ref.find('NTUC-UMS') <> -1:
		item = 'subscription'
	elif ref.find('CCC - 4147464002260895') <> -1:
		item = 'Citi'
	elif ref.find('M1 ') <> -1:
		item = '4G'
	elif ref.find('DBS VISA DEBIT CARD 5% CA SH') <> -1:
		item = 'cashback'
	elif code == 'ITR' and ref.find('TOP-UP TO PAYLAH') <> -1:
		item = 'paylah'
		
	return item

def citi_get_item(desc):
	item = 'others'
	
	if desc.find('AJISEN RAMEN') <> -1 or desc.find('MCDONALD') <> -1 or desc.find('STARBUCKS') <> -1 or desc.find('TEXAS CHICKEN') <> -1 or desc.find('DING TAI FUNG') <> -1 or desc.find('KFC') <> -1 or desc.find('SOUP SPOON') <> -1 or desc.find('SUBWAY') <> -1:
		item = 'F&B'
	elif desc.find('PYTHONANYWHERE') <> -1 or desc.find('FITNESS FIRST') <> -1 or desc.find('COURSERA') <> -1:
		item = 'subscription'
	elif desc.find('GRAB') <> -1 or desc.find('CITYCAB TAXI') <> -1:
		item = 'transport'
	elif desc.find('CASHBACK') <> -1:
		item = 'cashback'
	elif desc.find('LI RUNYUAN VISA DIRECT SG') <> -1:
		item = 'payment'
	elif desc.find('ALIPAY') <> -1 or desc.find('www.taobao.com') <> -1:
		item = 'online'
		
	return item