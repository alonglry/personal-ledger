from django.conf.urls import url, include

from . import views

app_name = 'test_ledger'

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^coa/$', views.coa, name='coa')
]