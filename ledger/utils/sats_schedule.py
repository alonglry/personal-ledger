#!/home/alonglry/.virtualenvs/django18/bin/python

##########################################################
#                                                        #
# file name: /ledger/utils/sats_schedule.py              #
# description: update lowerst and highest price for      #
#              stocks in stats_article                   #
# frequency: Daily 16:05                                 #
#                                                        #
##########################################################
#                                                        #
# version date       by              change              #
# 1.0     02/02/2017 Awai            initial release     #
#                                                        #
##########################################################

import sys
import os
from yahoo_finance import Share

sys.path.append('/home/alonglry/personal_finance')

from custom_admin import sqlexecute

def get_tickers():
	result = sqlexecute('SELECT distinct ticker_id FROM ledger_sats_article;')
	tmp = ''
	
	for r in result:
		tmp = tmp + "'" + r[0] + "',"
		
	#return tmp[:-1]
	return result
	
def get_date():
	import datetime
	tmp = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
	#tmp = datetime.date.today().strftime('%Y-%m-%d')
	return tmp
	
def if_trade(share,date,type):
	tmp = False
	
	if type == 'index':
		last_trade_date = share.get_trade_datetime()[:10]
		
		if last_trade_date == date: 
			tmp = True
		else:
			tmp = False
	elif type == 'stock':
		try:
			if share.get_historical(date,date) == []:
				tmp = False
			else:
				tmp = True
		except:
			tmp = False
		
	return tmp
	
def insert_stock_value(ticker,date,hist):
	
	sql = "SELECT %s FROM ledger_sats_article WHERE ticker_id = '%s';" % ('min_price,max_price',ticker)
	result = sqlexecute(sql)
	
	min = get_number(result[0][0])
	max = get_number(result[0][1])
	
	_volume,_adj,_close,_open,_high,_low = hist['Volume'],hist['Adj_Close'],hist['Close'],hist['Open'],hist['High'],hist['Low']
	
	if round(float(_high),4) > max: 
		sql = "UPDATE ledger_sats_article SET max_price = %s WHERE ticker_id = '%s';" % (_high,ticker)
		sqlexecute(sql)
		sql = "UPDATE ledger_sats_article SET max_price_date = '%s' WHERE ticker_id = '%s';" % (date,ticker)
		
		sqlexecute(sql)
		
		print '%s has updated max_price & max_price_date for %s.' % (ticker,date)
	
	if min ==0 or round(float(_low),4) < min:
		sql = "UPDATE ledger_sats_article SET min_price = %s WHERE ticker_id = '%s';" % (_low,ticker)
		sqlexecute(sql)
		sql = "UPDATE ledger_sats_article SET min_price_date = '%s' WHERE ticker_id = '%s';" % (date,ticker)
		sqlexecute(sql)
		
		print '%s has updated min_price & min_price_date for %s.' % (ticker,date)
	
def get_number(amt):
	if str(amt) == 'None':
		return 0
	else:
		return float(amt)
	
################################################################
# name: get_stock
# type: function
# import by:
#
# use: get stock Date,Open,High,Low,Close,Adj.close,Volume as a
#      dictionary, return dummy if values cannot be found
#      this function is to be run in server
################################################################
# version author description                          date
# 1.0     awai   initial release                      29/02/2018
################################################################

def get_stock(ticker):
	import csv
	import urllib2
	from datetime import datetime,date
	
	try:
		url = 'https://query1.finance.yahoo.com/v7/finance/download/'+ticker+'?interval=1d&events=history&crumb=e07PO/.pmsl'
		req = urllib2.Request(url=url,data=b'None',headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
		response = urllib2.urlopen(req)
		read = csv.reader(response)

		for row in read:
			p = row

		a = {'date':datetime.strptime(p[0],'%Y-%m-%d'),'open':float(p[1]),'high':float(p[2]),'low':float(p[3]),'close':float(p[4]),'adj_close':float(p[5]),'volume':float(p[6]),'status':'success'}
	except:
		a = {'date':date.today(),'open':0.0,'high':0.0,'low':0.0,'close':0.0,'adj_close':0.0,'volume':0.0,'status':'fail'}
		
	return a

################################################################
# name: upadte
# type: function
# import by:
#
# use: upadte stock_value table
#      this function is to be run in server
################################################################
# version author description                          date
# 1.0     awai   initial release                      02/02/2017
# 1.1     awai   change method getting values         29/01/2018
################################################################
'''
def update():
	
	for r in get_tickers():
		ticker,share,today = r[0],Share(r[0]),get_date()
		
		if if_trade(share,today,'stock'):
	
			hist = share.get_historical(today,today)[0]
			
			insert_stock_value(ticker,today,hist)
			
		else:
			print '%s has no trading on %s.' % (ticker,today)
'''
def update():
	companies = sqlexecute('SELECT a.id,b.ticker,lower_price,upper_price,min_price_date,max_price_date,start_date,end_date FROM ledger_sats_article a,ledger_stock_company b WHERE a.ticker_id = b.id;')
	
	for r in companies:
		id,ticker,share = r[0],r[1],get_stock(r[1])
		
		if share['status'] == 'success' and r[7]>=share['date'].date():
			if share['high'] > r[3]:
				sqlexecute("UPDATE ledger_sats_article SET upper_price = '%s' WHERE id = '%s';" % (share['high'],id))
				sqlexecute("UPDATE ledger_sats_article SET max_price_date = '%s' WHERE id = '%s';" % (share['date'],id))
				
				print "update %s with upper price %s on %s" % (ticker,share['high'],share['date'])
				
			if share['low'] <r[2]:
				sqlexecute("UPDATE ledger_sats_article SET lower_price = '%s' WHERE id = '%s';" % (share['low'],id))
				sqlexecute("UPDATE ledger_sats_article SET min_price_date = '%s' WHERE id = '%s';" % (share['date'],id))
				
				print "update %s with lower price %s on %s" % (ticker,share['low'],share['date'])
	
################################################################
# name: upadte
# type: task
# import by: /home/alonglry/.virtualenvs/django18/bin/python /home/alonglry/personal_finance/ledger/utils/sats_schedule.py
#            daily at 16:05
#
# use: tigger update function
################################################################
# version author description                          date
# 1.0     awai   initial release                      02/02/2017
################################################################	

print '/ledger/utils/sats_schedule.py/'
update()

'''
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal_finance.settings")

import django

#django.setup()

from ledger import models

from ledger.models import sats_article
a=sats_article.objects.all()
print a
'''