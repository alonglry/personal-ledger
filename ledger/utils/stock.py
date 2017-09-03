from yahoo_finance import Share
import sys
from ..models import stock_company, stock_value, stock_dimension, stock_company_form, stock_dimension_form
from datetime import timedelta, date, datetime

def stock_get(attr=''):
	if attr == 'company_all':
		return stock_company.objects.all()
	elif attr == 'value_all':
		return stock_value.objects.all()
	elif attr == 'dimension_all':
		return stock_dimension.objects.all()
	elif attr == 'company_meta':
		return stock_company._meta
	elif attr == 'value_meta':
		return stock_value._meta
	elif attr == 'dimension_meta':
		return stock_dimension._meta
	elif attr == 'company_form':
		return stock_company_form()
	elif attr == 'dimension_form':
		return stock_dimension_form()
		
def stock_save(request,attr=''):
	if attr == 'company':
		form = stock_company_form(request.POST)
		if form.is_valid():
			form.save()
			
			#get exchange
			t = request.POST.get('ticker','')
			share = Share(t)
			e = share.get_stock_exchange()
			s = stock_company.objects.get(ticker=t)
			s.exchange = e
			s.save()
			
			#get all dates
			#i = share.get_info()
			#st,en = datetime.strptime(i['start'], '%Y-%m-%d'),datetime.strptime(i['end'], '%Y-%m-%d')
			#for n in range(int((en - st).days) + 1):
			#	d = st + timedelta(n)
			#	stock_value.objects.update_or_create(ticker=s,date=d,defaults={ticker:s,date:d})
			st = '1950-01-01'
			#en = datetime.date.today().strftime('%Y-%m-%d')
			en = share.get_trade_datetime()[:10]
			hi = share.get_historical(st,en)
			for h in hi:
				_d      = datetime.strptime(h['Date'], '%Y-%m-%d')
				_volume = h['Volume']
				_adj    = float(h['Adj_Close'])
				_high   = float(h['High'])
				_low    = float(h['Low'])
				_close  = float(h['Close'])
				_open   = float(h['Open'])
				stock_value.objects.update_or_create(ticker=s,date=_d,defaults={'volume':_volume,
																			 'adj_close':_adj,
																			  	  'high':_high,
																				   'low':_low,
																				 'close':_close,
																				  'open':_open})
	elif attr == 'dimension':
		form = stock_dimension_form(request.POST)
		if form.is_valid():
			form.save()		

##############################################################
# name: get_price
# type: function
# import by: ledger/models/account
#            ledger/models/sats
# use: get stock price
##############################################################
# version author description                      date
# 1.0     awai   initial release                  02/02/2017
##############################################################
def get_price(ticker):
	if str(ticker) == '(u\'\',)':
		price = None
	else:
		price = Share(t(ticker)).get_price()
	
	if price == None:
		price = 0
	else:
		price = float(price)
	return price
	
def t(ticker):
	st = str(ticker)
	st = st.replace("(u'",'').replace("',)",'')
	return st