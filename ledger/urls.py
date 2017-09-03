from django.conf.urls import url, include

from . import views

app_name = 'ledger'

urlpatterns = [
	#url(r'^$', views.index, name='index'),
	url(r'^accounts/$', views.accounts, name='accounts'),
	#url(r'^parameters/$', views.parameters, name='parameters'),
	url(r'^journals/$', views.journals, name='journals'),
	url(r'^sats/$',views.sats_handler, name='sats'),
	url(r'^sats/(?P<article_id>[0-9]+)/$',views.articles_handler, name='articles'),
	#url(r'^gls/$', views.gls, name='gls'),
	url(r'^journal_basic_expense/$',views.basic_expense_handler, name='basic'),
	url(r'^journal_vickers_journal_form/$',views.vickers_handler, name='vickers'),
	url(r'^journal_sos/$',views.sos_handler, name='sos'),
	url(r'^journal_cpf/$',views.cpf_handler, name='cpf'),
	url(r'^journal_journal_form/$',views.journal_journal_form, name='journal_journal_form'),
	url(r'^journal_fundsupermart/$',views.fundsupermart_handler, name = 'fundsupermart'),
	url(r'^journal_trips/$',views.trips_handler, name = 'trips'),
	url(r'^journal_setting/$',views.setting_handler, name = 'setting'),
	url(r'^sql',views.sql_handler,name='sql'),
	url(r'^transaction',views.transaction,name='transaction'),
	url(r'^check',views.balance_check_handler,name='check'),
	url(r'^stocks',views.stock_handler,name='stocks'),
	url(r'^logout',views.logout_handler,name='logout'),
	url(r'^login',views.login_handler,name='login'),
	url(r'^tables/$',views.tables,name='tables'),
	url(r'^tables/(?P<table_name>[\w]+)/$',views.individual_table,name='individual_table'),
	url(r'', include("social.apps.django_app.urls", namespace="social")),
	#url(r'^googlea39c8dec68b5dc01.html/',views.googlea39c8dec68b5dc01,name='googlea39c8dec68b5dc01')
]