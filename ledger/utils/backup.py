'''
select COLUMN_NAME from information_schema.columns
where table_schema = 'alonglry$stock'
and table_name = 'ledger_account_info';
'''
import sys
import os

#from django.conf import settings
#settings.configure()

os.environ['DJANGO_SETTINGS_MODULE'] = "personal_finance.personal_finance.settings"

from django.db import connection

tables = ['account_info']

for table in tables:
	m = table + '_m'
	
	query = "select COLUMN_NAME from information_schema.columns where table_schema = 'alonglry$stock' and table_name = '%s';" % table
	
	cursor = connection.cursor()
	cursor.execute(query)
	row = cursor.fetchone()