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

################################################################
# name: get_price
# type: function
# import by: ledger/models/account
#            ledger/models/sats
#						 ledger/views/accounts
#            ledger/views/sats
# use: get stock adj_close price and return as float for given
#      date. If no date given, get stock adj_close price for
#      current date. if stock not exists or no trading, throw 
#      RemoteDataError.
################################################################
# version author description                          date
# 1.0     awai   initial release                      02/02/2017
# 1.1     awai   getting price use pandas             12/11/2017
# 1.1     awai   throw IO error if ticker not found   19/11/2017
# 1.2     awai   getting price use urllib2				    26/11/2017
# 1.3     awai   getting price use pandas             27/12/2017
################################################################
def get_price(ticker,d = None):

	'''
	try:
		#price = Share(t(ticker)).get_price()
		import pandas as pd
		#import pandas.io.data as web 
		import pandas_datareader.data as web
		
		start = datetime(2017,11,1)
		end = date.today()
		s = web.DataReader(t(ticker), "google", start, end)
		price = s['Close'][len(s)-1]
		
		return price
	except:
		
	try:
		import csv
		import urllib2
		url = 'https://query1.finance.yahoo.com/v7/finance/download/'+t(ticker)+'?interval=1d&events=history&crumb=e07PO/.pmsl'
		req = urllib2.Request(url=url,data=b'None',headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
		response = urllib2.urlopen(req)
		read = csv.reader(response)

		for row in read:
			p = row

		price = float(p[5])

		return price
			
	except:		
		raise IOError(ticker + ' not found using either pandas or urilib2.    ' + url)
	'''

	from datetime import date
	import pandas as pd
	import pandas_datareader.data as web
	from pandas_datareader._utils import RemoteDataError
	
	if d == None:
		day = date.today()
	else:
		day = d
	
	try:
		df = web.DataReader(ticker, "yahoo", day,day)
	except RemoteDataError as err:
		raise RemoteDataError(err)
	
	return float(df.tail(1).iloc[:,0:].values[0][4])
	
def t(ticker):
	st = str(ticker)
	st = st.replace("(u'",'').replace("',)",'')
	return st

################################################################
# name: get_stock
# type: function
# import by: ledger/models/sats
#
# use: get stock Date,Open,High,Low,Close,Adj.close,Volume as a
#      dictionary
################################################################
# version author description                          date
# 1.0     awai   initial release                      29/02/2018
################################################################

def get_stock(ticker):
	import csv
	import urllib2
	url = 'https://query1.finance.yahoo.com/v7/finance/download/'+ticker+'?interval=1d&events=history&crumb=e07PO/.pmsl'
	req = urllib2.Request(url=url,data=b'None',headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
	response = urllib2.urlopen(req)
	read = csv.reader(response)

	for row in read:
		p = row

	a = {'date':datetime.strptime(p[0],'%Y-%m-%d'),'open':float(p[1]),'high':float(p[2]),'low':float(p[3]),'close':float(p[4]),'adj_close':float(p[5]),'volume':float(p[6])}
	return a