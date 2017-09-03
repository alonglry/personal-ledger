from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from ..forms import  vickers_journal_form, journal_form

#from vickers_handler import vickers_handler, vickers_mtm_handler
#from cpf_handler import cpf_handler
#from basic_handler import basic_handler, journal_handler
#from SOS_handler import SOS_handler
#from fundsupermart_handler import fundsupermart_handler

def journal_form_request_handler(request,action):
	if request.method == 'POST':
		if action == 'vickers':
			form = vickers_journal_form(request.POST)
		elif action == 'CPF':
			form = cpf_journal_form(request.POST)
		elif action == 'journal':
			form = journal_form(request.POST)
		#elif action == 'basic':
		#	form = basic_journal_form(request.POST)
		elif action == 'SOS':
			form = dbs_sos_journal_form(request.POST)
		#elif action == 'fundsupermart':
		#	form = fundsupermart_journal_form(request.POST)
			
		if form.is_valid():
		
			if action == 'vickers':
				if request.POST.get('choice','') == 'mtm':
					vickers_mtm_handler(request)
				else:
					vickers_handler(request)
			#elif action == 'CPF':
				#cpf_handler(request)
			elif action == 'basic':
				basic_handler(request)
			elif action == 'journal':
				journal_handler(request)
			elif action == 'SOS':
				SOS_handler(request)
			elif action ==  'fundsupermart':
				fundsupermart_handler(request)
					
			return HttpResponseRedirect(reverse('ledger:journals'))
		else:
			return HttpResponseRedirect(reverse('ledger:journals'))
	else:
		return HttpResponseRedirect(reverse('ledger:journals'))