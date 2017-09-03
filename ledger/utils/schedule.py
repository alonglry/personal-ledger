
#print __package__
#print __file__
import sys
import os
from os import path
print path.abspath(__file__)
print path.dirname( path.abspath('.')) 
print path.dirname( path.dirname( path.abspath('.')) )

#sys.path.append( path.dirname( path.dirname( path.abspath('.') ) )).append('/personal_finance')
#from django.conf
sys.path.append('/home/alonglry/personal_finance')


import personal_finance.settings
#settings.configure()

os.environ['DJANGO_SETTINGS_MODULE'] = "personal_finance.settings"

print 'hr'
#if __package__ is None:
	#sys.path.append('/home/alonglry/personal_finance/ledger/')

#from django.conf import settings
#settings.configure()

#from utils.ledger import test
	#print DJANGO_SETTINGS_MODULE
#import personal_finance.ledger
#from personal_finance import ledger
from home.alonglry.personal_finance.ledger import models

models.parameter(value_1='a',value_2='b').save()
#else:
#	from ..utils.ledger import test

print 'aaa'
'''
from stock import test

test()
'''