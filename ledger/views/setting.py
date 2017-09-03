from datetime import datetime, timedelta
from random import randint
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms

from ledger.models import parameter
from django.contrib.auth.models import User

#############################################################
# name: setting_journal_form
# type: form
# import by: ledger/view/init
# use: HTML form for settings
#############################################################
# version author description                      date
# 1.0     awai   initial release                  30/12/2016
#############################################################

class setting_journal_form(forms.Form):
	test_mode = forms.BooleanField()
	remove_test = forms.BooleanField(initial = False)
	

##############################################################
# name: setting_handler
# type: function
# import by: ledger/urls
# use: main view module for settings
##############################################################
# version author description                      date
# 1.0     awai   initial release                  27/12/2016
# 1.1     awai   add action for change mode       31/12/2016
# 1.2     awai   add change mode for account info 07/02/2017
##############################################################

def setting_handler(request):
	if request.method == 'POST':
		#return HttpResponse("Hello world.")
		
		id = request.POST.get('id','')
		error = ''
		
		if id == 'id_test_mode':
			
			try:
				a = request.POST.get('action','')
				tmp = parameter.objects.get(value_1='mode')
			
				if a == 'true':
					tmp.value_2 = 'test'
					tmp.save()
				elif a == 'false':
					tmp.value_2 = None
					tmp.save() 
			except:
				error = error + '\nupdate mode error'
				
			if error == '':
				return HttpResponse('success')
			else:
				return HttpResponse(error)
				
		elif id == 'id_remove_test':
			
			a = request.POST.get('action','')
				
			if a == 'true':
				from ledger.models import cashflow,account_info,investment_transaction,investment_info,journal,ledger
				
				try:	
					investment_transaction.remove_test()
				except:
					error = error + '\nremove investment transaction test error'
					
				try:	
					account_info.remove_test()
				except:
					error = error + '\nremove account info test error'
					
				try:	
					cashflow.remove_test()
				except:
					error = error + '\nremove cashflow test error'
					
				try:	
					journal.remove_test()
				except:
					error = error + '\nremove journal test error'
					
				try:
					investment_info.remove_test()
				except:
					error = error + '\nremove investment info error'
					
				if error == '':
					return HttpResponse('success')
				else:
					return HttpResponse(error)
			
		
	else:
		return HttpResponseRedirect(reverse('ledger:journals'))

