from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

from ledger.models import account_info,cashflow,parameter
from ledger.utils import user_name, device
from ledger.forms import transaction_form
from django.db.models import F,Sum,Avg,Max,Min

##############################################################
# name: transactions
# type: function
# import by: ledger/urls
#            ledger/views/_init_.py
# use: main view module for transaction (from source) page
##############################################################
# version author description                      date
# 1.0     awai   initial release                  23/07/2017
# 1.1     awai   add account_info as primary key  26/11/2017
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
		
		error = ''
		
		#get account info and cashflow
		try:
			ai = account_info.objects.filter(owner=user)
			c = cashflow.objects.filter(account_info__in=ai)
		except:
			error = error + '\naccount_info and cashflow get value having issue.'
			
		#use account info and cashflow to prepare data for template
		try:
			l = []
			i = c.order_by('item').values('item').distinct()
			d = c.order_by('year','month').values('year','month').distinct()
			f = c.order_by('item','year','month','currency').values('item','year','month','currency').annotate(amount = Sum('amount'))

			l.append(i)
			l.append(d)
			l.append(f)
				
		except:
			error = error + '\ncashflow prepare data having issue.'
			
		return render(request,'ledger/transaction.html',{'device':d,'textbox':transaction_form(),'user':user,'cashflow':l})

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
				ai = account_info.objects.get(company='POSB',owner=user,identifier='savings')
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
							account_info = ai,

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
							account_info = ai,

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
							account_info = ai,

							defaults={"mode": parameter.mode(),"item":word[7] if word[7] <> '' else dbs_get_item(word[1],word[4],word[5])}
						)
			#Citi dividend card
			elif text.strip() <> '' and company.strip() == 'Citi':
				ai = account_info.objects.get(company='Citi',owner=user)
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
						account_info = ai,

						defaults={"mode": parameter.mode(),"item":word[3] if (word[3] <> '' and word[3].find('SGD') <> 0) else citi_get_item(word[1])}
					)
			#CPF
			elif text.strip() <> '' and company.strip() == 'CPF':
				oai = account_info.objects.get(company='CPF',owner=user,identifier='ordinary')
				sai = account_info.objects.get(company='CPF',owner=user,identifier='special')
				mai = account_info.objects.get(company='CPF',owner=user,identifier='medisave')
				line = text.splitlines()
				
				for l in line:
					word = l.split("\t")
					if word[1] <> 'BAL':
						cashflow.objects.update_or_create(
							date = datetime.strptime(word[0],'%d %b %y'),							
							year = datetime.strptime(word[0],'%d %b %y').strftime('%Y'),
							month = datetime.strptime(word[0],'%d %b %y').strftime('%m'),
							amount = float(word[4].replace(',','')),
							company = 'CPF',
							owner = user,
							account = 'ordinary',
							currency = 'SGD',
							account_info = oai,
							item = word[1],
							mode = parameter.mode()
						)
						cashflow.objects.update_or_create(
							date = datetime.strptime(word[0],'%d %b %y'),							
							year = datetime.strptime(word[0],'%d %b %y').strftime('%Y'),
							month = datetime.strptime(word[0],'%d %b %y').strftime('%m'),
							amount = float(word[5].replace(',','')),
							company = 'CPF',
							owner = user,
							account = 'special',
							currency = 'SGD',
							account_info = sai,
							item = word[1],
							mode = parameter.mode()
						)
						cashflow.objects.update_or_create(
							date = datetime.strptime(word[0],'%d %b %y'),							
							year = datetime.strptime(word[0],'%d %b %y').strftime('%Y'),
							month = datetime.strptime(word[0],'%d %b %y').strftime('%m'),
							amount = float(word[6].replace(',','')),
							company = 'CPF',
							owner = user,
							account = 'medisave',
							currency = 'SGD',
							account_info = mai,
							item = word[1],
							mode = parameter.mode()
						)
				
		if error == '':
			return HttpResponse('success')
		else:
			return HttpResponse(error)
		
def dbs_get_item(code,ref,ref2):
	item = 'others'
	
	if code == 'PAY':
		item = 'salary'
	elif code == 'INT' or code == 'ADV':
		item = 'interest'
	elif code == 'AWL':
		item = 'cash'
	elif code == 'CDP' or ref.find('IFA -P0305995') <> -1 or ref.find('IFAST FINANCIAL') <> -1 or ref.find('SCB:0102046042') <> -1:
		item = 'investment'
	elif ref.find('HONGUO') <> -1 or ref.find('SUSHI') <> -1 or ref.find('KOUFU PTE LTD') <> -1 or ref.find('SOUP SPOON') <> -1 or ref.find('NTUC FOODFARE') <> -1 or ref.find('SPINELLI COFFEE') <> -1 or ref.find('96 BEVERAGE') <> -1 or ref.find('STARBUCKS') <> -1 or ref.find('CHILLIPADI') <> -1 or ref.find('KFC') <> -1 or ref.find('SHENGSIONG') <> -1 or ref.find('SHENG SIONG') <> -1 or ref.find('DIMBULAH') <> -1 or ref.find('PARIS BAGUETTE') <> -1 or ref.find('BREADTALK') <> -1 or ref.find('SHENG KEE DESSERT') <> -1 or ref.find('BURGER KING') <> -1 or ref.find('MCDONALD') <> -1:
		item = 'F&B'
	elif ref.find('MOBIKE') <> -1 or code == 'ACT' or ref2.find('TO: COMFORT TAXI') <> -1 or ref.find('TRANSIT LINK PTE LTD') <> -1 or ref.find('COMFORT TRANSPORTATION') <> -1 or ref.find('PREMIER TAXIS') <> -1 or ref.find('SMRT TAXIS') <> -1 or ref.find('TRANS-CAB SERVICES') <> -1 or ref.find('FINANCE DEPT-IBG') <> -1 or ref.find('COMFORT TAXI') <> -1:
		item = 'transport'
	elif ref.find('NTUC-UMS') <> -1:
		item = 'subscription'
	elif ref.find('CCC - 4147464002260895') <> -1 or ref.find('CCC - 4147465001630178') <> -1:
		item = 'Citi clearing'
	elif ref.find('CCC -5520380017962941') <> -1 or ref.find('CCC -5520380053181703') <> -1:
		item = 'POSB everyday clearing'
	elif ref.find('M1 ') <> -1:
		item = '4G'
	elif ref.find('DBS VISA DEBIT CARD 5% CA SH') <> -1:
		item = 'cashback'
	elif code == 'ITR' and ref.find('TOP-UP TO PAYLAH') <> -1:
		item = 'paylah'
	elif ref.find('HO-IGV') <> -1 or ref.find('GV ') <> -1:
		item = 'movie'
	elif ref.find('IRAS') <> -1:
		item = 'tax'
	elif ref.find('110-22109-6') <> -1:
		item = 'housing'
		
	return item

def citi_get_item(desc):
	item = 'others'
	
	if desc.find('AJISEN RAMEN') <> -1 or desc.find('MCDONALD') <> -1 or desc.find('SWENSEN') <> -1 or desc.find('BURGER KING') <> -1 or desc.find('DIMBULAH') <> -1 or desc.find('STARBUCKS') <> -1 or desc.find('TEXAS CHICKEN') <> -1 or desc.find('DING TAI FUNG') <> -1 or desc.find('KFC') <> -1 or desc.find('SOUP SPOON') <> -1 or desc.find('SUBWAY') <> -1 or desc.find('SHENG SIONG') <> -1:
		item = 'F&B'
	elif desc.find('PYTHONANYWHERE') <> -1 or desc.find('FITNESS FIRST') <> -1 or desc.find('COURSERA') <> -1:
		item = 'subscription'
	elif desc.find('GRAB') <> -1 or desc.find('CITYCAB TAXI') <> -1:
		item = 'transport'
	elif desc.find('CASHBACK') <> -1 or desc.find('REWARDS CASH REBATE') <> -1:
		item = 'cashback'
	elif desc.find('LI RUNYUAN VISA DIRECT SG') <> -1 or desc.find('CUI XIAOYU VISA DIRECT SG') <> -1:
		item = 'Citi clearing'
	elif desc.find('ALIPAY') <> -1 or desc.find('www.taobao.com') <> -1 or desc.find('Lazada') <> -1 or desc.find('AMAZON MKTPLACE') <> -1:
		item = 'online'
	elif desc.find('M1 LIMITED') <> -1:
		item = '4G'
	elif desc.find('MOBIKE') <> -1:
		item = 'transport'
	elif desc.find('LESSONSGOWHERE.COM') <> -1:
		item = 'entertainment'
		
	return item