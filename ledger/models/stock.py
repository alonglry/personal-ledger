import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F,Sum,Avg,Max,Min

###begining of stock_dimension###
class stock_dimension(models.Model):

	class Meta:
		verbose_name = 'stock dimension'

	alphas_num = models.CharField('101_formulaic_alphas_num',max_length=100,null=True,blank=True)
	alphas_type = models.CharField('101_formulaic_alphas_type',max_length=100,null=True,blank=True)
	data_type = models.CharField('data_type',max_length=100,null=True,blank=True)
	descr = models.CharField('description',max_length=500,null=True,blank=True)
	dim = models.CharField('dimension',max_length=100,unique=True)
	remark = models.CharField('remark',max_length=100,null=True,blank=True)
	src = models.CharField('source',max_length=100,null=True,blank=True)

	def __unicode__(self):
		return self.dim

###end of stock_dimension###
###end of stock_dimension customised###

###begining of stock_dimension_m###
class stock_dimension_m(models.Model):
	alphas_num = models.CharField(max_length=100,null=True,blank=True)
	alphas_type = models.CharField(max_length=100,null=True,blank=True)
	data_type = models.CharField(max_length=100,null=True,blank=True)
	descr = models.CharField(max_length=500,null=True,blank=True)
	dim = models.CharField(max_length=100,null=True,blank=True)
	remark = models.CharField(max_length=100,null=True,blank=True)
	src = models.CharField(max_length=100,null=True,blank=True)
	bk_date = models.DateField()
###end of stock_dimension_m###
###end of stock_dimension_form customised###

###begining of stock_dimension_form###
class stock_dimension_form(ModelForm):
	class Meta:
		model = stock_dimension
		fields = ['alphas_num','alphas_type','data_type','descr','dim','remark','src']
###end of stock_dimension_form###

###begining of stock_value###

class stock_value(models.Model):

	class Meta:
		verbose_name = 'stock value'

	volume = models.IntegerField('valume',validators=[MinValueValidator(0),MaxValueValidator(9999999999)],null=True,blank=True)
	change = models.DecimalField('change',max_digits=7,decimal_places=2,null=True,blank=True)
	prev_close = models.DecimalField('previous c',max_digits=7,decimal_places=2,null=True,blank=True)
	avg_daily_volume = models.DecimalField('avg daily volume',max_digits=7,decimal_places=2,null=True,blank=True)
	stock_exchange = models.DecimalField('stock exch',max_digits=7,decimal_places=2,null=True,blank=True)
	market_cap = models.CharField('market cap',max_length=10,null=True,blank=True)
	book_value = models.DecimalField('book value',max_digits=7,decimal_places=2,null=True,blank=True)
	ebitda = models.CharField('ebitda',max_length=10,null=True,blank=True)
	dividend_yield = models.DecimalField('dividend y',max_digits=7,decimal_places=2,null=True,blank=True)
	year_high = models.DecimalField('52w high',max_digits=7,decimal_places=2,null=True,blank=True)
	year_low = models.DecimalField('52w low',max_digits=7,decimal_places=2,null=True,blank=True)
	price_sales = models.DecimalField('price sale',max_digits=7,decimal_places=2,null=True,blank=True)
	price_book = models.DecimalField('price book',max_digits=7,decimal_places=2,null=True,blank=True)
	short_ratio = models.DecimalField('short rati',max_digits=7,decimal_places=2,null=True,blank=True)
	eps = models.DecimalField('earnings p',max_digits=7,decimal_places=2,null=True,blank=True)
	pe = models.DecimalField('price earn',max_digits=7,decimal_places=2,null=True,blank=True)
	peg = models.DecimalField('price earn',max_digits=7,decimal_places=2,null=True,blank=True)
	dps = models.DecimalField('dividend p',max_digits=7,decimal_places=2,null=True,blank=True)
	ticker = models.ForeignKey('stock_company',to_field='ticker',on_delete=models.CASCADE,null=True,blank=True,verbose_name='ticker')
	date = models.DateField('date',null=True,blank=True)
	tickerdate = models.CharField('ticker date identifier',max_length=20,null=True,blank=True,unique=True)
	open = models.DecimalField('open price',max_digits=7,decimal_places=2,null=True,blank=True)
	close = models.DecimalField('close pric',max_digits=7,decimal_places=2,null=True,blank=True)
	high = models.DecimalField('high',max_digits=7,decimal_places=2,null=True,blank=True)
	low = models.DecimalField('low',max_digits=7,decimal_places=2,null=True,blank=True)
	adj_close = models.DecimalField('adjusted close',max_digits=7,decimal_places=2,null=True,blank=True)

	def __unicode__(self):
		return self.ticker.ticker + ' ' + str(self.date)



###end of stock_value###

###begining of stock_company###

class stock_company(models.Model):

	class Meta:
		verbose_name = 'stock company'
		verbose_name_plural = 'stock companies'

	ticker = models.CharField('ticker',max_length=100,null=True,blank=True,unique=True)
	company = models.CharField('company',max_length=100,null=True,blank=True,unique=True)
	exchange = models.CharField('exchange',max_length=100,null=True,blank=True)
	country = models.CharField('country',max_length=100,null=True,blank=True)
	short_name = models.CharField('short name',max_length=100,null=True,blank=True)
	type = models.CharField('type',max_length=100,null=True,blank=True)
	remark = models.CharField('remark',max_length=500,null=True,blank=True)

	def __unicode__(self):
		return self.company + ' (' + self.ticker + ')'
	
	@property
	def name(self):
		if self.short_name <> None:
			name = self.short_name
		else:
			name = self.company
		
		return name
	
	@property
	def price(self):
		d = stock_value.objects.filter(ticker=self).aggregate(Max('date'))
		p = stock_value.objects.get(ticker=self,date=d['date__max']).close
		return p
		
	@property
	def currency(self):
		if self.exchange == 'SES':
			return 'SGD'
		elif self.exchange == 'HKEX':
			return 'HKD'
		else:
			return 'USD'
	
	@classmethod
	def add(self,ticker,company='',type=''):
		from yahoo_finance import Share
		share = Share(ticker)
		exchange = share.get_stock_exchange()
		if company == '' and type == '':
			try:
				obj = self.objects.create(ticker=ticker,exchange=exchange)
			except:
				obj = self.objects.get(ticker=ticker)
		else:
			try:
				obj = self.objects.create(company=company,type=type,ticker=ticker,exchange=exchange)
			except:
				obj = self.objects.get(ticker=ticker)
		return obj

class stock_company_form(ModelForm):
	class Meta:
		model = stock_company
		fields = ['ticker','company','country','short_name','type','remark']

class stock_company_m(models.Model):
	ticker = models.CharField(max_length=100,null=True,blank=True)
	company = models.CharField(max_length=100,null=True,blank=True)
	exchange = models.CharField(max_length=100,null=True,blank=True)
	country = models.CharField(max_length=100,null=True,blank=True)
	short_name = models.CharField(max_length=100,null=True,blank=True)
	type = models.CharField(max_length=100,null=True,blank=True)
	remark = models.CharField(max_length=500,null=True,blank=True)
	bk_date = models.DateField()

###end of stock_company###

###begining of stock_strategy###
class stock_strategy(models.Model):

	class Meta:
		verbose_name = 'stock strategy'
		verbose_name_plural = 'stock strategies'

	description = models.CharField(max_length=500,null=True,blank=True)
	remark = models.CharField(max_length=500,null=True,blank=True)
	state = models.CharField(max_length=100,null=True,blank=True,choices=(('plan','plan'),('build','build'),('simulate','simulate'),('use','use')))
	strategy = models.CharField(max_length=100,unique=True)

	def __unicode__(self):
		return self.strategy

###end of stock_strategy###
###end of stock_strategy customised###

###begining of stock_strategy_m###
class stock_strategy_m(models.Model):
	description = models.CharField(max_length=500,null=True,blank=True)
	remark = models.CharField(max_length=500,null=True,blank=True)
	state = models.CharField(max_length=100,null=True,blank=True)
	strategy = models.CharField(max_length=100,null=True,blank=True)
	bk_date = models.DateField()
###end of stock_strategy_m###
###end of stock_strategy_form customised###

###begining of stock_strategy_form###
class stock_strategy_form(ModelForm):
	class Meta:
		model = stock_strategy
		fields = ['description','state','strategy']
###end of stock_strategy_form###

