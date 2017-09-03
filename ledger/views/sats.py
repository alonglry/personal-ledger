import sys
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from ledger.utils import save_source, save_article

from ledger.models import stock_strategy_form,sats_article,sats_source,stock_company_form,stock_company,sats_source_form,sats_article_form

##############################################################
# name: sats_handler
# type: function
# import by: ledger/urls
# use: main view module for sats page
##############################################################
# version author description                      date
# 1.0     awai   initial release                  01/02/2017
# 1.1     awai   add error handling for article   13/02/2017
##############################################################

@login_required(login_url='/login/')
def sats_handler(request):
	#return HttpResponse("Hello, world. strategies")
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