#!/home/alonglry/.virtualenvs/django18/bin/python

##########################################################
#                                                        #
# file name: /ledger/utils/stock.py                      #
# description: insert latest stock information from      #
#              Yahoo                                     #
#                                                        #
##########################################################
#                                                        #
# version date       by              change              #
# 1.0     19/06/2016 Awai            initial release     #
# 1.1     19/02/2017 Awai            update tickerdate   #
#                                                        #
##########################################################

import sys
import os
from yahoo_finance import Share

sys.path.append('/home/alonglry/personal_finance')

from custom_admin import sqlexecute

def get_tickers():
	result = sqlexecute('SELECT distinct ticker FROM ledger_stock_company;')
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
		if share.get_historical(date,date) == []:
			tmp = False
		else:
			tmp = True
		
	return tmp

def if_new(ticker,date):
	sql = "SELECT * FROM ledger_stock_value WHERE ticker_id = '%s' AND date='%s';" % (ticker,date)
	result = sqlexecute(sql)
	
	if str(result) == '()':
		tmp = True
	else:
		tmp = False
		
	return tmp
	
def insert_stock_value(ticker,date,hist):
	_volume,_adj,_close,_open,_high,_low = hist['Volume'],hist['Adj_Close'],hist['Close'],hist['Open'],hist['High'],hist['Low']
	
	sql = "INSERT INTO ledger_stock_value (ticker_id,date,volume,adj_close,close,open,high,low) values ('%s','%s','%s','%s','%s','%s','%s','%s');" % (ticker,date,_volume,_adj,_close,_open,_high,_low)
	
	result = sqlexecute(sql)
	
def insert_index_value(ticker,date,share):
	_price = share.get_price()
	
	sql = "INSERT INTO ledger_stock_value (ticker_id,date,close) values ('%s','%s','%s');" % (ticker,date,_price)
	
	result = sqlexecute(sql)

def update_stock_value(ticker,date,hist):
	_volume,_adj,_close,_open,_high,_low = hist['Volume'],hist['Adj_Close'],hist['Close'],hist['Open'],hist['High'],hist['Low']
	
	sql = "UPDATE ledger_stock_value SET volume='%s',adj_close='%s',close='%s',open='%s',high='%s',low='%s' WHERE ticker_id='%s' AND date='%s';" % (_volume,_adj,_close,_open,_high,_low,ticker,date)
	
	result = sqlexecute(sql)
	
def update_index_value(ticker,date,share):
	_price = share.get_price()
	
	sql = "UPDATE ledger_stock_value SET close='%s' WHERE ticker_id='%s' AND date='%s';" % (_price,ticker,date)
	
	result = sqlexecute(sql)
	
def update_stock_value_others(ticker,date,share):
	tmp = ''
	tmp = tmp + "market_cap='%s'," % share.get_market_cap()
	tmp = tmp + "book_value='%s'," % share.get_book_value()
	tmp = tmp + "ebitda='%s'," % share.get_ebitda()
	#tmp = tmp + "dps='%s'," % share.get_dividend_share()
	#tmp = tmp + "dividend_yield='%s'," % share.get_dividend_yield()
	tmp = tmp + "eps='%s'," % share.get_earnings_share()
	tmp = tmp + "year_high='%s'," % share.get_year_high()
	tmp = tmp + "year_low='%s'," % share.get_year_low()
	tmp = tmp + "pe='%s'," % share.get_price_earnings_ratio()
	tmp = tmp + "peg='%s'," % share.get_price_earnings_growth_ratio()
	tmp = tmp + "price_sales='%s'," % share.get_price_sales()
	tmp = tmp + "price_book='%s'," % share.get_price_book()
	tmp = tmp + "short_ratio='%s'," % share.get_short_ratio()
	tmp = tmp + "tickerdate='%s'" % ticker + '_' + str(date)
	
	sql = "UPDATE ledger_stock_value SET %s WHERE ticker_id='%s' AND date='%s';" % (tmp,ticker,date)
	
	result = sqlexecute(sql)

def update():
	for r in get_tickers():
		ticker,share,today = r[0],Share(r[0]),get_date()
		
		if ticker not in ('500SGD.SI'):
		
			if if_trade(share,today,'stock'):
		
				hist = share.get_historical(today,today)[0]
				
				if if_new(ticker,today):
					insert_stock_value(ticker,today,hist)
					print '%s has been inserted ticker,date,volume,adj_close,close,open,high,low for %s.' % (ticker,today)
				else:
					update_stock_value(ticker,today,hist)
					print '%s has been updated volume,adj_close,close,open,high,low for %s.' % (ticker,today)
				
				update_stock_value_others(ticker,today,share)
				print '%s has been updated other fields for %s.' % (ticker,today)
				
			else:
				print '%s has no trading on %s.' % (ticker,today)
				
		else:
			if if_trade(share,today,'index'):
				if if_new(ticker,today):
					insert_index_value(ticker,today,share)
					print '%s has been inserted ticker,date,close for %s.' % (ticker,today)
				else:
					update_index_value(ticker,today,share)
					print '%s has been updated close for %s.' % (ticker,today)
			else:
				print '%s has no trading on %s.' % (ticker,today)
		
	
update()