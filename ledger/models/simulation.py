import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F,Sum,Avg,Max,Min

###begining of stock_value_simulation###
class stock_value_simulation(models.Model):

	class Meta:
		verbose_name = 'simulation value'

	adj_close = models.DecimalField('adjusted close price',max_digits=7,decimal_places=2,null=True,blank=True)
	close = models.DecimalField('close price',max_digits=7,decimal_places=2,null=True,blank=True)
	date = models.DateField('date',null=True,blank=True)
	high = models.DecimalField('high',max_digits=7,decimal_places=2,null=True,blank=True)
	low = models.DecimalField('low',max_digits=7,decimal_places=2,null=True,blank=True)
	open = models.DecimalField('open price',max_digits=7,decimal_places=2,null=True,blank=True)
	ticker = models.ForeignKey('stock_company_simulation',to_field='ticker',on_delete=models.PROTECT,null=True,blank=True,verbose_name='ticker')
	volume = models.IntegerField('valume',validators=[MinValueValidator(0),MaxValueValidator(9999999999)],null=True,blank=True)
###end of stock_value_simulation###
###end of stock_value_simulation customised###

###begining of stock_company_simulation###
class stock_company_simulation(models.Model):

	class Meta:
		verbose_name = 'simulation company'

	company = models.CharField('company',max_length=100,null=True,blank=True,unique=True)
	country = models.CharField('country',max_length=100,null=True,blank=True)
	exchange = models.CharField('exchange',max_length=100,null=True,blank=True)
	remark = models.CharField('remark',max_length=500,null=True,blank=True)
	short_name = models.CharField('short name',max_length=100,null=True,blank=True)
	ticker = models.CharField('ticker',max_length=100,null=True,blank=True,unique=True)
	type = models.CharField('type',max_length=100,null=True,blank=True,choices=(('company','company'),('index','index')))

	def __unicode__(self):
		return self.company + ' (' + self.ticker + ')'

###end of stock_company_simulation###
###end of stock_company_simulation customised###

