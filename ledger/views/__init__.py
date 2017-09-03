from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from django.db.models import F
from django.contrib.auth.decorators import login_required

from ledger.models import investment_transaction, parameter, investment_info
from ledger.models.GL import journal
from ledger.models.account import account_info,account_info_form,cashflow_form


from ..forms import vickers_journal_form, journal_form
from ledger.views.fundsupermart import fundsupermart_journal_form
#from ledger.views.basic_expense import basic_journal_form
from ledger.views.trips import trips_journal_form
from ledger.views.sos import dbs_sos_journal_form
from ledger.views.cpf import cpf_journal_form
from ledger.views.setting import setting_journal_form

from ledger.custormised_views.journal_form_request_handler import journal_form_request_handler

from sats import *
from sql import sql_handler
from stock import stock_handler
from cpf import cpf_handler
from accounts import accounts
from sos import sos_handler
from login import *
from basic_expense import *
from balance_check import *
from fundsupermart import *
from all_table_columns import *
from vickers import *
from trips import *
from setting import *
from transaction import *
from error_page import *

td = datetime.now().strftime("%Y-%m-%d")

'''
def index(request):
    #return HttpResponse("Hello, world. ledger")
	#return HttpResponse(request.META.get('HTTP_USER_AGENT', '').lower())
	return HttpResponse(request.get_full_path())
	
def googlea39c8dec68b5dc01(request):
	return render(request,'ledger/googlea39c8dec68b5dc01.html')

def accounts(request):
	if request.method == 'POST':
		form = account_info_form(request.POST)
		if form.is_valid():
			i = None if request.POST.get('identifier','') == '' else request.POST.get('identifier','')
			n = None if request.POST.get('number','') == '' else request.POST.get('number','')
			c = None if request.POST.get('company','') == '' else request.POST.get('company','')
			o = None if request.POST.get('owner','') == '' else request.POST.get('owner','')
			ct = None if request.POST.get('country','') == '' else request.POST.get('country','')
			t = None if request.POST.get('type','') == '' else request.POST.get('type','')
			s = None if request.POST.get('status','') == '' else request.POST.get('status','')
			cu = None if request.POST.get('currency','') == '' else request.POST.get('currency','')
			
			account_info(identifier=i,number=n,company=c,owner=o,country=ct,type=t,status=s,currency=cu).save()
			return HttpResponseRedirect(reverse('ledger:accounts'))
		else:
			return HttpResponseRedirect(reverse('ledger:accounts'))
	else:
		accounts = account_info.objects.exclude(type = 'shares')
		investments = investment_info.objects.exclude(identifier = '')
		cf = cashflow.objects.all()
	return render(request,'ledger/accounts.html',{'accounts':accounts,'investments':investments,'cf':cf})

def parameters(request):
	if request.method == 'POST':
		form = parameterForm(request.POST)
		if form.is_valid():
			v1 = None if request.POST.get('value_1','') == '' else request.POST.get('value_1','')
			v2 = None if request.POST.get('value_2','') == '' else request.POST.get('value_2','')
			v3 = None if request.POST.get('value_3','') == '' else request.POST.get('value_3','')
			v4 = None if request.POST.get('value_4','') == '' else request.POST.get('value_4','')
			v5 = None if request.POST.get('value_5','') == '' else request.POST.get('value_5','')
			
			parameter(value_1=v1,value_2=v2,value_3=v3,value_4=v4,value_5=v5).save()
			return HttpResponseRedirect(reverse('ledger:parameters'))
		else:
			return HttpResponseRedirect(reverse('ledger:parameters'))
	else:
	    #title = parameter._meta.verbose_name.title()
	    parameters = parameter.objects.all()
	    forms = parameterForm()
	return render(request,'ledger/parameters.html',{'parameters':parameters,'forms':forms})

def gls(request):
	if request.method == 'POST':
		form = gl_infoForm(request.POST)
		if form.is_valid():
			i = None if request.POST.get('identifier','') == '' else request.POST.get('identifier','')
			b = None if request.POST.get('balancesheet_type','') == '' else request.POST.get('balancesheet_type','')
			t = None if request.POST.get('asset_type','') == '' else request.POST.get('asset_type','')
			h = None if request.POST.get('asset_holder','') == '' else request.POST.get('asset_holder','')
			s = None if request.POST.get('asset_source','') == '' else request.POST.get('asset_source','')
			l1 = None if request.POST.get('level_1_category','') == '' else request.POST.get('level_1_category','')
			l2 = None if request.POST.get('level_2_category','') == '' else request.POST.get('level_2_category','')
			
			gl_info(identifier=i,balancesheet_type=b,asset_type=t,asset_holder=h,asset_source=s,level_1_category=l1,level_2_category=l2).save()
			return HttpResponseRedirect(reverse('ledger:gls'))
		else:
			return HttpResponseRedirect(reverse('ledger:gls'))
	else:
		gls = gl_info.objects.all()
		#le = ledger.objects.all()
		forms = gl_infoForm()
        return render(request,'ledger/gls.html',{'gls':gls,'forms':forms})#,'ledger':le})
'''
@login_required(login_url='/login/')
def journals(request):
	if request.META.get('HTTP_USER_AGENT', '').lower().find("iphone") > 0:
		device = 'phone'
	else:
		device = 'others'
		
	user = request.user.username
	td = datetime.now().strftime("%Y-%m-%d") #current day date
	journals = journal.objects.filter(last_update_date = td,owner=get_owner(user))
	#basic_form = basic_journal_form()
	vickers_form = vickers_journal_form()
	sos_form = dbs_sos_journal_form()
	cpf_form = cpf_journal_form()
	
	#return HttpResponse("Hello, world. journal")
	return render(request,'ledger/journals.html',{'basic_form':cashflow_form(),
	                                            'vickers_form':vickers_form,
																									'sos_form':sos_form,
																									'journals':journals,
																									'cpf_form':cpf_form,
																							'journal_form':journal_form(),
																								'trips_form':trips_journal_form(),
																				'fundsupermart_form':fundsupermart_journal_form(),
																											'user':user,
																						 'basic_expense':parameter.get('basic expense',get_owner(user)),
																							'setting_form':setting_journal_form(initial={'test_mode':True if parameter.mode()=='test' else False}),
																										'device':device
																									})

#def journal_dbs_sos_journal_form(request):
#	return journal_form_request_handler(request,'SOS')
def get_owner(user):
	if user == 'xgg' or user == 'alonglry':
		owner = 'Awai'
	elif user == 'xqq':
		owner = 'Serena'
	else:
		owner = 'others'
	return owner
	
#def journal_vickers_journal_form(request):
#	return journal_form_request_handler(request,'vickers')

#def journal_cpf_journal_form(request):
#	return journal_form_request_handler(request,'CPF')

def journal_basic_journal_form(request):
	return journal_form_request_handler(request,'basic')

def journal_journal_form(request):
	return journal_form_request_handler(request,'journal')
	
#def journal_fundsupermart(request):
#	return journal_form_request_handler(request,'fundsupermart')

def test(request):
	obj = journal.objects.filter(gl_account_id = 'POSB savings')
	t='a'
	for a in obj:
		t=t+'e'
	return HttpResponse(t)