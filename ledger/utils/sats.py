import sys
from ..models import sats_source, sats_article, sats_source_form, sats_article_form

def get_source(attr = ''):
	if attr == 'all':
		return sats_source.objects.all()
	elif attr == 'meta':
		return sats_source._meta
	elif attr == 'form':
		return sats_source_form()

def get_article(attr = ''):
	if attr == 'all':
		return sats_article.objects.all()
	elif attr == 'meta':
		return sats_article._meta
	elif attr == 'form':
		return sats_article_form()
	else:
		return sats_article.objects.filter(id = attr)	
		
def save_source(request):
	form = sats_source_form(request.POST)
	if form.is_valid():
		form.save()
		
	'''
	try:
		sats_source(src   = getValue(request,'src'),
					descr = getValue(request,'descr'),
					url   = getValue(request,'url')).save()
	except:   
		exc_type, exc_value, exc_traceback = sys.exc_info()
		return exc_type.__name__.replace('Error',' Error') + ': ' + exc_value.message
	'''
		
def save_article(request):
	
	form = sats_article_form(request.POST,request.FILES)
	if form.is_valid():			
		form.save()
	
	#update history price url
	'''
	a = sats_article.objects.filter(ticker=getValue(request,'ticker'))
	for o in a:
		o.trend = 'http://chart.finance.yahoo.com/t?s=%s&lang=en-US&region=US&width=600&height=360' % getValue(request,'ticker')
		o.save()
	'''
	#update total count for this source	
	a = sats_article.objects.filter(src=getValue(request,'src')).count()
	s = sats_source.objects.get(src=getValue(request,'src'))
	s.total_count = a
	s.save()
	
	'''
	try:
		sats_article(src          = getValue(request,'src'),
					 product      = getValue(request,'product'),
					 product_type = getValue(request,'product_type'),
					 ticker       = getValue(request,'ticker'),
					 trend        = 'http://chart.finance.yahoo.com/t?s=%s&lang=en-US&region=US&width=600&height=360' % getValue(request,'ticker'),
					 strategy     = getValue(request,'strategy'),
					 descr        = getValue(request,'descr'),
					 url          = getValue(request,'url'),
					 #screenshot   = getValue(request,'screenshot'),
					 #screenshot   = sats_article_form(request.POST,request.FILES).cleaned_data['screenshot'],
					 validation   = getValue(request,'validation'),
					 start_date   = getValue(request,'start_date'),
					 end_date     = getValue(request,'end_date'),
					 ror          = getValue(request,'ror'),
					 status       = getValue(request,'status')).save()
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		return exc_type.__name__.replace('Error',' Error') + ': ' + exc_value.message
	'''
	
def getValue(request,field):
	tmp = request.POST.get(field,'')
	return tmp