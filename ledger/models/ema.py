import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F,Sum,Avg,Max,Min


###begining of ema_value###

class ema_value(models.Model):

	class Meta:
		verbose_name = 'stock EMA value'

	tickerdate = models.ForeignKey('stock_value',to_field='tickerdate',on_delete=models.PROTECT,null=True,blank=True,unique=True,verbose_name='ticker date identifier')
	ticker = models.ForeignKey('stock_company',to_field='ticker',on_delete=models.PROTECT,null=True,blank=True,verbose_name='ticker')
	ema5 = models.DecimalField('5 day EMA',max_digits=7,decimal_places=2,null=True,blank=True)
	ema10 = models.DecimalField('10 day EMA',max_digits=7,decimal_places=2,null=True,blank=True)

	def __unicode__(self):
		return self.tickerdate
	
	@classmethod
	def get_tickerdate(self,t=None):
		from ledger.models import stock_value, stock_company
	
		if t <> 'all':
			c = stock_value.objects.filter(ticker=t)
			c1 = stock_company.objects.get(ticker=t)
		else:
			c = stock_value.objects.all()
	
		for cc in c:
			try:
				self.objects.create(tickerdate=cc,ticker=c1)
			except IntegrityError:
				continue
	
	@classmethod
	def get_ema(self,t=None,d=None):
		from ledger.models import stock_value
	
		if t <> 'all':
			t1 = self.objects.filter(ticker=t)



###end of ema_value###
