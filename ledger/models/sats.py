import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F,Sum,Avg,Max,Min

###begining of sats_source###

class sats_source(models.Model):

	class Meta:
		verbose_name = 'stock article tracking source'
		ordering = ['src']

	src = models.CharField('source',max_length=100,unique=True)
	url = models.URLField('URL',null=True,blank=True)
	descr = models.CharField('descriptio',max_length=100,null=True,blank=True)
	lud_dt = models.DateField('last update date',auto_now=True,null=True,blank=True)

	def __unicode__(self):
		return self.src
	
	@property
	def total_count(self):
	    return sats_article.objects.filter(src=self).count()
	
	@property
	def fail_count(self):
	    return sats_article.objects.filter(src=self,status='fail').count()
	
	@property
	def success_count(self):
	    return sats_article.objects.filter(src=self,status='success').count()
	
	@classmethod
	def add(self,s,d,u=''):
	    obj = self.objects.create(src=s,descr=d,url=u)
	    return obj
	
	@classmethod
	def update(self,i,c,v):
	    obj = self.objects.get(id=i)
	    obj.__dict__.update({c:v})
	    obj.save()
	
	@classmethod
	def get(self,source=''):
		obj = self.objects.get(src=source)
		return obj

class sats_source_form(ModelForm):
	class Meta:
		model = sats_source
		fields = ['src','url','descr']

class sats_source_m(models.Model):
	src = models.CharField(max_length=100,null=True,blank=True)
	url = models.URLField(null=True,blank=True)
	descr = models.CharField(max_length=100,null=True,blank=True)
	lud_dt = models.DateField(null=True,blank=True)
	bk_date = models.DateField()

###end of sats_source###

###begining of sats_article###

class sats_article(models.Model):

	class Meta:
		verbose_name = 'stock article tracking article'

	date = models.DateField('date',null=True,blank=True)
	src = models.ForeignKey('sats_source',to_field='src',on_delete=models.PROTECT,verbose_name='source')
	ticker = models.ForeignKey('stock_company',to_field='ticker',on_delete=models.PROTECT,verbose_name='ticker')
	strategy = models.ForeignKey('stock_strategy',to_field='strategy',on_delete=models.PROTECT,null=True,blank=True,verbose_name='strategy')
	start_date = models.DateField('start date',null=True,blank=True)
	end_date = models.DateField('end date',null=True,blank=True)
	initial_price = models.DecimalField('initial price',max_digits=9,decimal_places=4,null=True,blank=True)
	lower_price = models.DecimalField('lower price',max_digits=9,decimal_places=4,null=True,blank=True)
	upper_price = models.DecimalField('upper price',max_digits=9,decimal_places=4,null=True,blank=True)
	currency = models.CharField('currency',max_length=10,null=True,blank=True)
	status = models.CharField('status',max_length=100,null=True,blank=True)
	min_price = models.DecimalField('min price',max_digits=9,decimal_places=4,null=True,blank=True)
	min_price_date = models.DateField('min price date',null=True,blank=True)
	max_price = models.DecimalField('max price',max_digits=9,decimal_places=4,null=True,blank=True)
	max_price_date = models.DateField('max price date',null=True,blank=True)

	def __unicode__(self):
		return self.ticker.ticker + ' ' + self.src.src
	
	@classmethod
	def update(self,i,c,v):
		obj = self.objects.get(id=i)
		obj.__dict__.update({c:v})
		obj.save()
		
	@classmethod
	def add(self,source,company,lower_price=None,upper_price=None,currency=None,start_date=None,end_date=None,initial_price=None):
		start_date = None if start_date == '' else start_date
		obj = self.objects.create(src=source,ticker=company,lower_price=lower_price,upper_price=upper_price,currency=currency,start_date=start_date,end_date=end_date,initial_price=initial_price)
			
		return obj
			
	@classmethod
	def get(self,attr=''):
		if attr == 'all':
			return self.objects.all()
		elif attr == 'meta':
			return self._meta
		else:
			return self.objects.filter(id = attr)
				
	@property
	def earning(self):
		if self.initial_price <> None:
			price = self.current_price
			return round((price - float(self.initial_price)) * 1000 - 12.5*2,2)
	
	@property
	def current_price(self):
		try:
			from ledger.utils.stock import get_price
			price = get_price(self.ticker.ticker)
			return price
		except:
			return None
	
	@property
	def increase(self):
		try:
			return (float(self.current_price) / float(self.initial_price) - 1) * 100
		except:
			return None
	
	@property
	def adj_increase(self):
		try:
			unit = 1000 / (float(self.initial_price) * 1.05)
			current_price = float(self.current_price) * 0.95 * unit - 12.5 #5% bid spread & $12.5 commission per $1000
			initial_price = 1000 + 12.5  #5% ask spread & $12.5 commission per $1000
			return (float(current_price) / float(initial_price) - 1) * 100
		except:
			return None
	
	@property
	def low_ror(self):
		if self.min_price <> None and self.initial_price <> None and self.initial_price <> 0:
			d = (self.min_price_date - self.start_date).total_seconds()/60/60/24/365
			import math
			r = (math.exp(math.log(self.min_price/self.initial_price,math.e) / d) - 1) * 100
	
			return r
		else:
			return None
	
	@property
	def adj_low_ror(self):
		if self.min_price <> None and self.initial_price <> None and self.initial_price <> 0:
			d = (self.min_price_date - self.start_date).total_seconds()/60/60/24/365
			unit = 1000 / (float(self.initial_price) * 1.05)
			initial_price = 1000 + 12.5  #5% ask spread & $12.5 commission per $1000
			current_price = float(self.min_price) * 0.95 * unit - 12.5 #5% bid spread & $12.5 commission per $1000
			import math
			r = (math.exp(math.log(current_price/initial_price,math.e) / d) - 1) * 100
	
			return r
		else:
			return None
	
	@property
	def high_ror(self):
		if self.max_price <> None and self.initial_price <> None and self.initial_price <> 0:
			d = (self.max_price_date - self.start_date).total_seconds()/60/60/24/365
			import math
			r = (math.exp(math.log(self.max_price/self.initial_price,math.e) / d) - 1) * 100
	
			return r
		else:
			return None
	
	@property
	def adj_high_ror(self):
		if self.max_price <> None and self.initial_price <> None and self.initial_price <> 0:
			d = (self.max_price_date - self.start_date).total_seconds()/60/60/24/365
			unit = 1000 / (float(self.initial_price) * 1.05)
			initial_price = 1000 + 12.5  #5% ask spread & $12.5 commission per $1000
			current_price = float(self.max_price) * 0.95 * unit - 12.5 #5% bid spread & $12.5 commission per $1000
			import math
			r = (math.exp(math.log(current_price/initial_price,math.e) / d) - 1) * 100
	
			return r
		else:
			return None

class sats_article_form(ModelForm):
	class Meta:
		model = sats_article
		fields = ['date','src','ticker','strategy','start_date','end_date','initial_price','lower_price','upper_price','currency','status']

class sats_article_m(models.Model):
	date = models.DateField(null=True,blank=True)
	src_id = models.CharField(max_length=100,null=True,blank=True)
	ticker_id = models.CharField(max_length=100,null=True,blank=True)
	strategy_id = models.CharField(max_length=500,null=True,blank=True)
	start_date = models.DateField(null=True,blank=True)
	end_date = models.DateField(null=True,blank=True)
	initial_price = models.DecimalField(max_digits=9,decimal_places=4,null=True,blank=True)
	lower_price = models.DecimalField(max_digits=9,decimal_places=4,null=True,blank=True)
	upper_price = models.DecimalField(max_digits=9,decimal_places=4,null=True,blank=True)
	currency = models.CharField(max_length=10,null=True,blank=True)
	status = models.CharField(max_length=100,null=True,blank=True)
	min_price = models.DecimalField(max_digits=9,decimal_places=4,null=True,blank=True)
	min_price_date = models.DateField(null=True,blank=True)
	max_price = models.DecimalField(max_digits=9,decimal_places=4,null=True,blank=True)
	max_price_date = models.DateField(null=True,blank=True)
	bk_date = models.DateField()

###end of sats_article###

###begining of sats_barchart###
class sats_barchart(models.Model):

	class Meta:
		verbose_name = 'barchart source'
		ordering = ['date','ticker']

	ticker = models.ForeignKey('stock_company',to_field='ticker',on_delete=models.PROTECT,verbose_name='ticker')
	t1 = models.CharField('today opinion',max_length=5,null=True,blank=True)
	y1 = models.CharField('yesterday opinion',max_length=5,null=True,blank=True)
	w1 = models.CharField('last week opinion',max_length=5,null=True,blank=True)
	m1 = models.CharField('last month opinion',max_length=5,null=True,blank=True)
	t2 = models.DecimalField('today opinion change',max_digits=4,decimal_places=2,null=True,blank=True)
	y2 = models.DecimalField('yesterday opinion change',max_digits=4,decimal_places=2,null=True,blank=True)
	w2 = models.DecimalField('last week opinion change',max_digits=4,decimal_places=2,null=True,blank=True)
	m2 = models.DecimalField('last month opinion change',max_digits=4,decimal_places=2,null=True,blank=True)
	date = models.DateField('date',null=True,blank=True)


###end of sats_barchart###
###end of sats_barchart customised###

###begining of sats_barchart_m###
class sats_barchart_m(models.Model):
	ticker_id = models.CharField(max_length=100,null=True,blank=True)
	t1 = models.CharField(max_length=5,null=True,blank=True)
	y1 = models.CharField(max_length=5,null=True,blank=True)
	w1 = models.CharField(max_length=5,null=True,blank=True)
	m1 = models.CharField(max_length=5,null=True,blank=True)
	t2 = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
	y2 = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
	w2 = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
	m2 = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
	date = models.DateField(null=True,blank=True)
	bk_date = models.DateField()
###end of sats_barchart_m###
###end of sats_barchart_form customised###

