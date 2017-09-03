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

def update():
	
	for r in get_tickers():
		ticker,share,today = r[0],Share(r[0]),get_date()
		
		if if_trade(share,today,'stock'):
	
			hist = share.get_historical(today,today)[0]
			
			insert_stock_value(ticker,today,hist)
			
		else:
			print '%s has no trading on %s.' % (ticker,today)
		
	
try:
	print '/ledger/utils/sats_schedule.py/'
	update()
except:
	print '/ledger/utils/sats_schedule.py/'
	print 'update fail'
	
'''
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal_finance.settings")

import django

#django.setup()

from ledger import models

from ledger.models import sats_article
a=sats_article.objects.all()
print a
'''