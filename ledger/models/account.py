import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F,Sum,Avg,Max,Min

###begining of account_info###

class account_info(models.Model):

	class Meta:
		verbose_name = 'account detail'
		verbose_name_plural = 'account details'
		ordering = ['company','identifier']

	company = models.CharField('company',max_length=50,null=True,blank=True)
	identifier = models.CharField('account identifier',max_length=50,null=True,blank=True)
	number = models.CharField('account number',max_length=50,null=True,blank=True)
	type = models.CharField('type',max_length=50,null=True,blank=True)
	status = models.CharField('status',max_length=50,default="active",null=True,blank=True)
	amount = models.DecimalField('account balance',max_digits=8,decimal_places=2,default=0,null=True,blank=True)
	currency = models.CharField('currency',max_length=10,default="SGD",null=True,blank=True)
	country = models.CharField('country',max_length=50,default="Singapore",null=True,blank=True)
	owner = models.CharField('owner',max_length=50,default="Awai",null=True,blank=True)
	remark = models.CharField('remark',max_length=100,null=True,blank=True)

	def __unicode__(self):
		return self.company + ': ' + self.identifier
	
	@classmethod
	def get(self,attr='',user=''):
		if attr == 'all':
			return self.objects.filter(owner=user).exclude(type = 'shares').exclude(type='funds')
		elif attr == 'meta':
			return self._meta
		elif attr == 'company':
			return self.objects.filter(owner=user).exclude(type = 'shares').exclude(type='funds').order_by('company').values('company').distinct()
		elif attr == 'cao':
			return self.objects.filter(owner=user).exclude(type = 'shares').exclude(type='funds').order_by('company','identifier','owner').values('company','identifier','owner').distinct()
		elif attr == 'checkbs':
			a = self.objects.filter(owner=user)\
			.exclude(type = 'shares' or 'insurance')\
			.order_by('company','identifier','currency')\
			.values('company','identifier','currency')\
			.annotate(amount = Sum('amount'))
	
			return a
			'''
				l = []
				for aa in a:
					l.append([aa.company + ' ' + aa.identifier,aa.currency,aa.amount])
	
				return l
				'''
	@classmethod
	def update(self,c,a,user,amount,r=None):
		#self.objects.filter(company=c,identifier=a,owner=get_owner(user)).update(amount=F('amount')+amount)
		#self.objects.update_or_create(company=c,identifier=a,owner=get_owner(user), defaults={'amount':F('amount')+amount})
		try:
			self.objects.filter(company=c,identifier=a,owner=user).update(amount=F('amount')+amount,remark=r)
			#tmp = self.objects.get(company=c,identifier=a,owner=get_owner(user))
			#tmp.amount = tmp.amount + amount
			#tmp.save()
		except:
			self.objects.create(company=c,identifier=a,owner=user,amount=amount,remark=r)
				
		return self.objects.filter(company=c,identifier=a,owner=user)
	
	@classmethod
	def remove_test(self):
		rows=self.objects.exclude(remark=None).exclude(remark='')
		for r in rows:
			try:
				r.amount = float(r.amount) - float(r.remark)
				r.remark = None
				r.save()
			except:
				1==1
	
	@property
	def balance(self):
		from ledger.models import cashflow
		balance = cashflow.objects.filter(account_info = self).aggregate(Sum('amount'))['amount__sum']
		
		return balance

class account_info_form(ModelForm):
	class Meta:
		model = account_info
		fields = ['company','identifier','number','type','status','amount','currency','country','owner','remark']

class account_info_m(models.Model):
	company = models.CharField(max_length=50,null=True,blank=True)
	identifier = models.CharField(max_length=50,null=True,blank=True)
	number = models.CharField(max_length=50,null=True,blank=True)
	type = models.CharField(max_length=50,null=True,blank=True)
	status = models.CharField(max_length=50,null=True,blank=True)
	amount = models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
	currency = models.CharField(max_length=10,null=True,blank=True)
	country = models.CharField(max_length=50,null=True,blank=True)
	owner = models.CharField(max_length=50,null=True,blank=True)
	remark = models.CharField(max_length=100,null=True,blank=True)
	bk_date = models.DateField()

###end of account_info###

###begining of cashflow###

class cashflow(models.Model):

	class Meta:
		verbose_name = 'cashflow'
		ordering = ['year','month']

	date = models.DateField('date',null=True,blank=True)
	year = models.IntegerField('year')
	month = models.IntegerField('month')
	company = models.CharField('company',max_length=50)
	account = models.CharField('account',max_length=50)
	item = models.CharField('item',max_length=50)
	currency = models.CharField('currency',max_length=10)
	amount = models.DecimalField('amount',max_digits=11,decimal_places=5)
	owner = models.CharField('owner',max_length=50)
	journal_id = models.CharField('journal ID',max_length=100,null=True,blank=True)
	detail = models.CharField('detail',max_length=200,null=True,blank=True)
	mode = models.CharField('mode',max_length=50,null=True,blank=True)
	account_info = models.ForeignKey('account_info',on_delete=models.CASCADE,verbose_name='account information')

	def __unicode__(self):
			return str(self.year) + '-' + str(self.month) + ' ' + self.company + ' ' + self.account + ' ' + self.item
	
	@classmethod
	def get(self,attr='',para='',user=''):
		if attr == 'all':
			l = []
			for p in para:
				
				try:
					c = str(p['company'])
				except:
					c = p['company']
				try:
					a = str(p['identifier'])
				except:
					a = p['identifier']
				try:
					o = str(p['owner'])
				except:
					o = p['owner']
	
				i = self.objects.filter(company=c,account=a,owner=o).order_by('item').values('item').distinct()
				f = self.objects.filter(company=c,account=a,owner=o).order_by('item','year','month').values('company','account','owner','item','year','month','currency').annotate(amount = Sum('amount'))				
				d = self.objects.filter(company=c,account=a,owner=o).order_by('year','month').values('year','month').distinct()				
				l.append([c,a,i,d,f])
			return l
		elif attr == 'checkbs':
			a = self.objects.filter(owner=user)\
			.order_by('company','account','currency')\
			.values('company','account','currency')\
			.annotate(amount = Sum('amount'))
				
			return a
	
	@classmethod
	def add(self,d,c,a,i,user,amt,ccy,j,m=None):
		if amt <> 0:
			self.objects.create(date = d,
								year = datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%Y'),
							   month = datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%m'),
							 company = c,
							 account = a,
								item = i,
							   owner = user,
							  amount = amt,
							currency = ccy,
						  journal_id = j,
								mode = m)
	
	@classmethod
	def remove_test(self):
		self.objects.filter(mode='test').delete()

class cashflow_form(ModelForm):
	class Meta:
		model = cashflow
		fields = ['date','year','month','company','account','item','currency','amount','detail']

class cashflow_m(models.Model):
	date = models.DateField(null=True,blank=True)
	year = models.IntegerField(null=True,blank=True)
	month = models.IntegerField(null=True,blank=True)
	company = models.CharField(max_length=50,null=True,blank=True)
	account = models.CharField(max_length=50,null=True,blank=True)
	item = models.CharField(max_length=50,null=True,blank=True)
	currency = models.CharField(max_length=10,null=True,blank=True)
	amount = models.DecimalField(max_digits=11,decimal_places=5,null=True,blank=True)
	owner = models.CharField(max_length=50,null=True,blank=True)
	journal_id = models.CharField(max_length=100,null=True,blank=True)
	detail = models.CharField(max_length=200,null=True,blank=True)
	mode = models.CharField(max_length=50,null=True,blank=True)
	account_info_id = models.IntegerField(null=True,blank=True)
	bk_date = models.DateField()

###end of cashflow###

###begining of investment_info###

class investment_info(models.Model):

	class Meta:
		verbose_name = 'investment account detail'
		verbose_name_plural = 'investment account details'
		ordering = ['company','identifier']

	broker_company = models.CharField('broker company',max_length=50,null=True,blank=True)
	account = models.CharField('broker account',max_length=50,null=True,blank=True)
	company = models.CharField('company',max_length=50,null=True,blank=True)
	identifier = models.CharField('ticker',max_length=50)
	type = models.CharField('type',max_length=50,null=True,blank=True,choices=(('shares','shares'),('funds','funds')))
	current_price = models.DecimalField('current price',max_digits=11,decimal_places=5,default=0,null=True,blank=True)
	unit = models.DecimalField('unit',max_digits=11,decimal_places=5,default=0,null=True,blank=True)
	commission = models.DecimalField('commission',max_digits=11,decimal_places=5,default=0,null=True,blank=True)
	dividend = models.DecimalField('dividend',max_digits=11,decimal_places=5,default=0,null=True,blank=True)
	currency = models.CharField('currency',max_length=10,null=True,blank=True)
	paid_amount = models.DecimalField('purchasing cost',max_digits=11,decimal_places=5,default=0,null=True,blank=True)
	sold_amount = models.DecimalField('selling income',max_digits=11,decimal_places=5,default=0,null=True,blank=True)
	total_yield = models.DecimalField('yield',max_digits=11,decimal_places=5,default=0,null=True,blank=True)
	last_update_amount = models.DecimalField('last update amount',max_digits=11,decimal_places=5,default=0,null=True,blank=True)
	country = models.CharField('country',max_length=50,null=True,blank=True)
	owner = models.CharField('owner',max_length=50)
	remark = models.CharField('remark',max_length=1000,null=True,blank=True)

	def __unicode__(self):
		return str(self.company) + ': ' + str(self.identifier)
	
	@classmethod
	def get_shares_info(self,ticker,user):
		o = user
		c = 'SG' if ticker[-3:] == '.SI' else 'others'
		info = self.objects.get_or_create(identifier=ticker,owner=o,defaults={'country':c,'unit':0,'last_update_amount':0,'paid_amount':0,'sold_amount':0,'company':''})
		info = self.objects.get(identifier=ticker,owner=o)
		return info
		
	@classmethod
	def sum_current_amount(self,user):
		#return round(float(self.objects.filter(owner=user).aggregate(Sum('current_amount'))['current_amount__sum']),2)
		from ledger.models import investment_info
		result = 0
		a = investment_info.objects.filter(owner=user)
		for aa in a:
			result = result + aa.current_amount
	
		return result
	
	@property
	def avg_buy_price(self):
		from ledger.models import investment_transaction
		amount = investment_transaction.objects.filter(owner=self.owner,identifier=self.identifier,transaction_type_1='actual',transaction_type_2='buy').aggregate(Sum('amount'))['amount__sum']
		unit = investment_transaction.objects.filter(owner=self.owner,identifier=self.identifier,transaction_type_1='actual',transaction_type_2='buy').aggregate(Sum('unit'))['unit__sum']
		
		if unit <> 0:
			return abs(amount / unit)
		else:
			return 0
	    
	@property
	def avg_sell_price(self):
		from ledger.models import investment_transaction
		amount = investment_transaction.objects.filter(owner=self.owner,identifier=self.identifier,transaction_type_1='actual',transaction_type_2='sell').aggregate(Sum('amount'))['amount__sum']
		unit = investment_transaction.objects.filter(owner=self.owner,identifier=self.identifier,transaction_type_1='actual',transaction_type_2='sell').aggregate(Sum('unit'))['unit__sum']
		
		if unit <> 0:
			return abs(amount / unit)
		else:
			return 0
	
	@property
	def price(self):
		from ledger.utils.stock import get_price
		price = get_price(self.identifier)
		
		if price == 0:
			price = float(self.current_price)
	
		return price
	
	@property
	def current_amount(self):
		return float(self.unit) * float(self.price)
	
	@property
	def profit_loss(self):
		return float(self.current_amount) - float(self.paid_amount) + float(self.sold_amount)
	
	@property
	def total_profit_loss(self):
		return float(self.profit_loss) - float(self.commission) + float(self.dividend)
	
	@property
	def ror(self):
		from ledger.models import investment_transaction
		cashflow=investment_transaction.objects.filter(owner=self.owner,identifier=self.identifier).order_by('date').values('date','amount')
		from ledger.models import investment_transaction
		from ledger.utils.algorithm import yield_calculation
	
		return - yield_calculation(cashflow)
	
	@property
	def dict_test_mode(self):
		d = {}
		d['remark']             = 'test'
		d['current_amount']     = str(self.current_amount)
		d['current_price']      = str(self.current_price)
		d['unit']               = str(self.unit)
		d['commission']         = str(self.commission)
		d['dividend']           = str(self.dividend)
		d['paid_amount']        = str(self.paid_amount)
		d['sold_amount']        = str(self.sold_amount)
		d['profit_loss']        = str(self.profit_loss)
		d['total_profit_loss']  = str(self.total_profit_loss)
		d['total_yield']        = str(self.total_yield)
		d['last_update_amount'] = str(self.last_update_amount)
		
		return d
		 	
	@classmethod
	def get(self,attr='',user=''):
		if attr == 'cao':
			return self.objects.filter(owner=user).exclude(identifier='').order_by('company','identifier','owner').values('company','identifier','owner').distinct()
		elif attr == 'all':
			return self.objects.filter(owner=user).exclude(identifier = '')
		elif attr == 'checkbs':
			a = self.objects.filter(owner=user)\
			.order_by('broker_company','account','currency')\
			.values('broker_company','account','currency')\
			.annotate(amount = Sum('current_amount'))
	
			return a
		#return specific company, key is ticker and owner, if not exists, create the company
		else:
			o = user
			ticker = attr
			try:
				obj = self.objects.get(identifier=ticker,owner=o)
			except:
				if ticker[-3:].upper() == '.SI':
					c = 'SG'
				else:
					c = 'others'
				#create in stock_company table
				from ledger.models import stock_company
				stock_company.add(ticker)
				#create in investment_info table
				obj = self.objects.create(identifier=ticker,country=c,owner=o)
			return obj
	
	@classmethod
	def remove_test(self):
		a = self.objects.exclude(remark__isnull=True).exclude(remark__exact='')
	
		for aa in a:
			d = aa.remark.replace("'",'').replace('{','').replace('}','').split(', ')
	        
			if d[0].split(': ')[0] == 'remark' and d[0].split(': ')[1] == 'test':
				x = {}
				for dd in d:
					x[dd.split(': ')[0]] = dd.split(': ')[1]
			
				aa.current_amount     = float(x['current_amount'])
				aa.current_price      = float(x['current_price'])
				aa.unit               = float(x['unit'])
				aa.commission         = float(x['commission'])
				aa.dividend           = float(x['dividend'])
				aa.paid_amount        = float(x['paid_amount'])
				aa.sold_amount        = float(x['sold_amount'])
				aa.profit_loss        = float(x['profit_loss'])
				aa.total_profit_loss  = float(x['total_profit_loss'])
				aa.total_yield        = float(x['total_yield'])
				aa.last_update_amount = float(x['last_update_amount'])
				aa.remark             = None
				aa.save()
	        

class investment_info_form(ModelForm):
	class Meta:
		model = investment_info
		fields = ['broker_company','account','company','identifier','type','country','owner']

class investment_info_m(models.Model):
	broker_company = models.CharField(max_length=50,null=True,blank=True)
	account = models.CharField(max_length=50,null=True,blank=True)
	company = models.CharField(max_length=50,null=True,blank=True)
	identifier = models.CharField(max_length=50,null=True,blank=True)
	type = models.CharField(max_length=50,null=True,blank=True)
	current_price = models.DecimalField(max_digits=11,decimal_places=5,null=True,blank=True)
	unit = models.DecimalField(max_digits=11,decimal_places=5,null=True,blank=True)
	commission = models.DecimalField(max_digits=11,decimal_places=5,null=True,blank=True)
	dividend = models.DecimalField(max_digits=11,decimal_places=5,null=True,blank=True)
	currency = models.CharField(max_length=10,null=True,blank=True)
	paid_amount = models.DecimalField(max_digits=11,decimal_places=5,null=True,blank=True)
	sold_amount = models.DecimalField(max_digits=11,decimal_places=5,null=True,blank=True)
	total_yield = models.DecimalField(max_digits=11,decimal_places=5,null=True,blank=True)
	last_update_amount = models.DecimalField(max_digits=11,decimal_places=5,null=True,blank=True)
	country = models.CharField(max_length=50,null=True,blank=True)
	owner = models.CharField(max_length=50,null=True,blank=True)
	remark = models.CharField(max_length=1000,null=True,blank=True)
	bk_date = models.DateField()

###end of investment_info###

###begining of investment_transaction###

class investment_transaction(models.Model):

	class Meta:
		verbose_name = 'investment transaction'
		verbose_name_plural = 'investment transaction'
		ordering = ['date','identifier','transaction_type_1','transaction_type_2']

	date = models.DateField('date')
	broker_company = models.CharField('broker company',max_length=50,null=True,blank=True)
	account = models.CharField('broker account',max_length=50,null=True,blank=True)
	identifier = models.CharField('ticker',max_length=50)
	amount = models.DecimalField('amount',max_digits=10,decimal_places=5,null=True,blank=True)
	currency = models.CharField('currency',max_length=10,null=True,blank=True)
	price = models.DecimalField('price',max_digits=10,decimal_places=5,null=True,blank=True)
	unit = models.DecimalField('unit',max_digits=10,decimal_places=5,null=True,blank=True)
	transaction_type_1 = models.CharField('transaction type 1',max_length=50,null=True,blank=True)
	transaction_type_2 = models.CharField('transaction type 2',max_length=50,null=True,blank=True)
	journal_id = models.CharField('journal ID',max_length=100,null=True,blank=True)
	owner = models.CharField('owner',max_length=50)
	remark = models.CharField('remark',max_length=500,null=True,blank=True)
	investment_info = models.ForeignKey('investment_info',on_delete=models.CASCADE,verbose_name='investment information')
	mode = models.CharField('mode',max_length=50,null=True,blank=True)

	def __unicode__(self):
		return self.identifier
	
	@classmethod
	def clear_simulation(self,ticker,user,m=None):
		try:
			if m == 'test':
				self.objects.filter(identifier=ticker,transaction_type_1='simulating',owner=user,mode=m).delete()
			else:
				self.objects.filter(identifier=ticker,transaction_type_1='simulating',owner=user).delete()
		except:
			pass
				
	@classmethod	
	def add(self,d,i,t1,t2,u,p,a,c,j,user,m=None,b=None,acc=None):
		self.objects.create(date = d,identifier = i,transaction_type_1 = t1,transaction_type_2 = t2,unit = u,price = p,amount = a,currency = c,journal_id = j,owner = user,mode = m,broker_company = b,account = acc)
						  
	@classmethod
	def get_transaction(self,attr='',para=''):
		if attr == 'all':
			l = []
			for p in para:
				try:
					c = str(p['company'])
				except:
					c = p['company']
				try:
					a = str(p['identifier'])
				except:
					a = p['identifier']
				try:
					o = str(p['owner'])
				except:
					o = p['owner']
				
				i = self.objects.filter(identifier=a,transaction_type_1='actual',owner=o).order_by('transaction_type_2').values('transaction_type_2').distinct()
				f = self.objects.filter(identifier=a,transaction_type_1='actual',owner=o).order_by('transaction_type_2','date')	
				d = self.objects.filter(identifier=a,transaction_type_1='actual',owner=o).order_by('date').values('date').distinct()	
				l.append([c,a,i,d,f])
			return l
	
	@classmethod
	def remove_test(self):
		self.objects.filter(mode='test').delete()
		self.objects.filter(transaction_type_1='simulating_test').transaction_type_1 = 'simulating'


class investment_transaction_m(models.Model):
	date = models.DateField(null=True,blank=True)
	broker_company = models.CharField(max_length=50,null=True,blank=True)
	account = models.CharField(max_length=50,null=True,blank=True)
	identifier = models.CharField(max_length=50,null=True,blank=True)
	amount = models.DecimalField(max_digits=10,decimal_places=5,null=True,blank=True)
	currency = models.CharField(max_length=10,null=True,blank=True)
	price = models.DecimalField(max_digits=10,decimal_places=5,null=True,blank=True)
	unit = models.DecimalField(max_digits=10,decimal_places=5,null=True,blank=True)
	transaction_type_1 = models.CharField(max_length=50,null=True,blank=True)
	transaction_type_2 = models.CharField(max_length=50,null=True,blank=True)
	journal_id = models.CharField(max_length=100,null=True,blank=True)
	owner = models.CharField(max_length=50,null=True,blank=True)
	remark = models.CharField(max_length=500,null=True,blank=True)
	investment_info_id = models.IntegerField(null=True,blank=True)
	mode = models.CharField(max_length=50,null=True,blank=True)
	bk_date = models.DateField()

###end of investment_transaction###
