import sys
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from ledger.utils import save_source, save_article, user_name, device

from ledger.models import stock_strategy_form,sats_article,sats_source,stock_company_form,stock_company,sats_source_form,sats_article_form,stock_strategy

##############################################################
# name: sats_handler
# type: function
# import by: ledger/urls
# use: main view module for sats page
##############################################################
# version author description                      date
# 1.0     awai   initial release                  01/02/2017
# 1.1     awai   add error handling for article   13/02/2017
# 1.2     awai   add mobile view                  28/12/2017
##############################################################

@login_required(login_url='/login/')
def sats_handler(request):
	#return HttpResponse("Hello, world. strategies")
	
	try:
		d = device(request)
	except Exception as err:
		return render(request,'ledger/error_page.html',{'device':'phone','message':err.args[0]})	

	try:
		user = user_name(request)
	except Exception as err:
		return render(request,'ledger/error_page.html',{'device':d,'message':err.args[0]})
	
	#mobile view
	if d == 'phone':
		if request.method == 'POST':
		
			if request.POST.get('name','') == 'article':
				from decimal import Decimal
				s = request.POST.get('src','')
				a = sats_source.objects.get(id = s)
				b = sats_article.objects.filter(src=a)
				
				tmp = ''
				
				for bb in b:
					tmp = tmp + '<p>' + bb.ticker.name + ' (' + bb.ticker.ticker + ') </br> ' \
					      + '<span class="date">' + str(bb.start_date) + '</span> ' \
						    + '<b>$' + str(round(bb.initial_price,2)) \
					      + '</b> <span class="' + ('green' if bb.upper_price > bb.initial_price * Decimal(1.05) else 'red') + '">' + str(round(bb.upper_price,2)) \
						    + '</b> <span class="' + ('green' if bb.lower_price > bb.initial_price * Decimal(1.05) else 'red') + '">' + str(round(bb.lower_price,2)) + '</span></p>'
				
				return HttpResponse(tmp)
			elif request.POST.get('name','') == 'source' and len(request.POST.get('src','')) <> 0:
				s = request.POST.get('src','')
				a = sats_source.objects.all().filter(src__icontains=s)
				tmp = ''
				
				if len(a) > 0:
					
					for aa in a:
						tmp = tmp + '<span class="sideSource" id="' + str(aa.id) + '">' + aa.src + '</span></br>'
					
				return HttpResponse(tmp)
			elif request.POST.get('name','') == 'stock':
				from lxml import html
				import requests
				c = request.POST.get('src','')
				c = 'http://d.yimg.com/aq/autoc?query=%s&region=US&lang=en-USs' % c #&callback=YAHOO.util.ScriptNodeDataSource.callback
				page = requests.get(c).content
				
				content = page[page.find('"Result":[')+11:-4]
				content = content.split('},{')
				
				tmp = ''
				
				if len(content) > 1:
					for cc in content:
						#a = cc.split(',')
						#tmp = tmp + '<p class="sideStock" id="' + a[0].split(':')[1] + '">' + a[1].split(':')[1] + ' (<b>' + a[0].split(':')[1] + '</b>) ' + a[4].split(':')[1] + ' (' + a[5].split(':')[1] + ')</p>'
						a = '{'+cc+'}'
						import json
						json_acceptable_string = a.replace("'", "\"")
						d = json.loads(json_acceptable_string)
						tmp = tmp + '<p class="sideStock" id="' + str(d['symbol']) + '">' + str(d['name']) + ' (<b>' + str(d['symbol']) + '</b>) ' + str(d['exchDisp']) + ' (' + str(d['typeDisp']) + ')</p>'
				tmp = tmp.replace('"','')
				
				
				return HttpResponse(tmp)
			elif request.POST.get('name','') == 'create':
				s = sats_source.objects.get_or_create(src=request.POST.get('src',''))
				a = request.POST.get('article','').split(' (')
				c = a[1].split(') ')[1]
				e = None
				cu = None
				
				if c == 'Singapore':
					e = 'SES'
				elif c == 'Hong Kong':
					e = 'HKEX'
				elif c[:4] == 'NYSE':
					e = 'NYSE'
					c == 'US'
				elif c == 'NASDAQ':
					e = 'NASDAQ'
					c = 'US'
				
				if c == 'Singapore':
					cu = 'SDG'
				elif c == 'US':
					cu = 'USD'
				elif c == 'Hong Kong':
					cu = 'HKD'
				
				t = stock_company.objects.get_or_create(ticker=a[1].split(') ')[0],company=a[0],country=c,exchange=e,type=a[2].replace(')',''))
				st = stock_strategy.objects.get(strategy='sats');
				
				from datetime import date, timedelta
				from ledger.utils import get_price,get_stock
				#p = get_price(t[0].ticker)
				p = get_stock(t[0].ticker) 
				
				a = sats_article.objects.get_or_create(src=s[0],ticker=t[0],strategy=st,date=p['date'],start_date=date.today(),min_price_date=p['date'],max_price_date=p['date'],end_date=date.today() + timedelta(90),lower_price=p['adj_close'],upper_price=p['adj_close'],initial_price=p['adj_close'])
				
				return HttpResponse('success')
			else:
				return HttpResponse('')
				
		else:
			s = sats_source.objects.all().values('src','descr','url','id')
			
			return render(request,'ledger/sats.html',{'device':d, 'source':s})
	
	#desktop view	
	else:	
		if request.method == 'POST':
			if getValue(request,'name') == 'source':

				d = request.POST.get('descr','')
				s = request.POST.get('src','')
				u = request.POST.get('url','')
				obj = sats_source.add(s,d,u)
				#return HttpResponseRedirect(reverse('ledger:sats'))
				return HttpResponse(obj.id)
				'''
				response_data = {}
				response_data['result'] = 'Create post successful!'
				response_data['postpk'] = post.pk
				response_data['text'] = post.text
				response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
				response_data['author'] = post.author.username
				return HttpResponse(json.dumps(response_data),content_type="application/json")
				'''
			elif getValue(request,'name') == 'article':		
				#save_article(request)
				error = ''

				try:
					company = request.POST.get('company','')
					type = request.POST.get('type','')
					ticker = request.POST.get('ticker','')

					source = sats_source.objects.get(src=request.POST.get('src',''))
					description = None #request.POST.get('descr','')
					url = request.POST.get('url','')
					screenshot = None #request.POST.get('screenshot','')
					validation = None #request.POST.get('validation','')
					lower_price = None #request.POST.get('lower_price','')
					upper_price = None #request.POST.get('upper_price','')
					currency = request.POST.get('currency','')
					start_date = request.POST.get('start_date','')
					end_date = None #request.POST.get('end_date','')
					initial_price = request.POST.get('initial_price','')
				except:
					error = error + '\nsats article get post request error'

				try:
					company = stock_company.add(ticker,company,type)
				except:
					error = error + '\ncreate new company error'

				#from yahoo_finance import Share
				#initial_price = round(float(Share(ticker).get_price()),2)

				try:
					obj = sats_article.add(source,company,description,url,screenshot,validation,lower_price,upper_price,currency,start_date,end_date,initial_price)
				except:
					error = error + '\ncreate new article error'

				if error == '':
					#return HttpResponseRedirect(reverse('ledger:sats'))
					return HttpResponse(obj.id)
				else:
					return HttpResponse(error)
			else:
				t = request.POST.get('table','')
				i = request.POST.get('id','')
				c = request.POST.get('column','')
				v = request.POST.get('value','')

				if t == 'sats_source_update':
					sats_source.update(i,c,v)
					return HttpResponse('%s %s %s %s' % (i,t,c,v))
				elif t == 'sats_article_update':
					sats_article.update(i,c,v)
					return HttpResponse('%s %s %s %s' % (i,t,c,v))
				elif t == 'sats_article_delete':
					sats_article.objects.get(id=i).delete()
					return HttpResponse('sats_article row %s is deleted' % i)
				elif t == 'sats_company_get':
					from lxml import html
					import requests
					c = 'http://d.yimg.com/aq/autoc?query=%s&region=US&lang=en-USs' % c #&callback=YAHOO.util.ScriptNodeDataSource.callback
					page = requests.get(c).content
					content = page[page.find('"Result":[')+11:-4]
					return HttpResponse(page)
				elif t == 'get_current_price':
					from yahoo_finance import Share
					return HttpResponse(round(float(Share(i).get_price()),2))
		else:
			error = ''

			try:
				sv = sats_source._meta
			except:
				error = error + '\nsats source get source verbose error.'

			try:
				s = sats_source.objects.all()
			except:
				error = error + '\nsats source get objects error.'

			try:
				sf = sats_source_form()
			except:
				error = error + '\nsats source get form error.'

			try:
				av = sats_article._meta
			except:
				error = error + '\nsats article get source verbose error.'

			try:
				a = sats_article.objects.all()
			except:
				error = error + '\nsats article get objects error.'

			try:
				af = sats_article_form()
			except:
				error = error + '\nsats article get form error.'

			try:
				ssf = stock_strategy_form()
			except:
				error = error + '\nstock strategy get form error.'

			try:
				scf = stock_company_form()
			except:
				error = error + '\nstock company get form error.'

			if error == '':
				return render(request,'ledger/sats.html',{'source_verbose'  : sv,
															'source'          : s,
															'source_form'     : sf,
															'article_verbose' : av,
															'article'         : a,
															'article_form'    : af,
															'form'            : ssf,
															'company_form'    : scf
															})
			else:
				return HttpResponse(error)
														
def articles_handler(request,article_id):
	a = get_article(article_id)	
	return render(request,'ledger/articles.html',{'article' : a})
	
def getValue(request,field):
	tmp = None if request.POST.get(field,'') == '' else request.POST.get(field,'')
	return tmp