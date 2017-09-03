import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F,Sum,Avg,Max,Min

###begining of journal###

class journal(models.Model):

	class Meta:
		verbose_name = 'journal'
		verbose_name_plural = 'journals'

	date = models.DateField('date')
	year = models.IntegerField('year',null=True,blank=True)
	month = models.IntegerField('month',null=True,blank=True)
	balancesheet_type = models.CharField('ledger type',max_length=50,choices=(('asset','asset'),('liability','liability'),('income','income'),('expense','expense')))
	activity_category = models.CharField('activity category',max_length=50,null=True,blank=True)
	activity = models.CharField('activity',max_length=50)
	account = models.CharField('account',max_length=50,null=True,blank=True)
	gl_account = models.CharField('GL account',max_length=50)
	amount = models.DecimalField('amount',max_digits=8,decimal_places=2)
	currency = models.CharField('currency',max_length=3)
	reference = models.CharField('reference',max_length=100)
	journal_id = models.CharField('journal ID',max_length=100,null=True,blank=True)
	owner = models.CharField('owner',max_length=50)
	post_indicator = models.CharField('post indicator',max_length=5,null=True,blank=True)
	remark = models.CharField('remark',max_length=100,null=True,blank=True)
	last_update_date = models.DateField('last update date',auto_now=True,null=True,blank=True)
	mode = models.CharField('mode',max_length=50,null=True,blank=True)

	def __unicode__(self):
		return '%s %s' % (self.date, self.reference)
	
	@classmethod
	def add(self,d,a,c,b,ac,acc,r,ai,g,j,user,m=None):
		if a <> 0:
			self.objects.create(date = d,
							    year = datetime.datetime.strptime(d,'%Y-%m-%d').strftime('%Y'),
							   month = datetime.datetime.strptime(d,'%Y-%m-%d').strftime('%m'),
							  amount = a,
							currency = c,
				   balancesheet_type = b,
						    activity = ac,
				   activity_category = acc,
						   reference = r,
						     account = ai,
						  gl_account = g,
						  journal_id = j,
							   owner = user,
	                            mode = m)
		
	@classmethod
	def get(self,attr='',user=''):
		if attr == 'checkbs':
			return self.objects.filter(owner=user,post_indicator='Y',balancesheet_type='asset' or 'liability')\
			.order_by('balancesheet_type','gl_account','account','currency')\
			.values('balancesheet_type','gl_account','account','currency')\
			.annotate(amount = Sum('amount'))
		elif attr == 'checkpl':
			return self.objects.filter(owner=user,post_indicator='Y')\
			.exclude(balancesheet_type='asset' or 'liability')\
			.order_by('balancesheet_type','currency')\
			.values('balancesheet_type','currency')\
			.annotate(amount = Sum('amount'))
	
	@classmethod
	def remove_test(self):
		self.objects.filter(mode='test').delete()


class journal_m(models.Model):
	date = models.DateField(null=True,blank=True)
	year = models.IntegerField(null=True,blank=True)
	month = models.IntegerField(null=True,blank=True)
	balancesheet_type = models.CharField(max_length=50,null=True,blank=True)
	activity_category = models.CharField(max_length=50,null=True,blank=True)
	activity = models.CharField(max_length=50,null=True,blank=True)
	account = models.CharField(max_length=50,null=True,blank=True)
	gl_account = models.CharField(max_length=50,null=True,blank=True)
	amount = models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
	currency = models.CharField(max_length=3,null=True,blank=True)
	reference = models.CharField(max_length=100,null=True,blank=True)
	journal_id = models.CharField(max_length=100,null=True,blank=True)
	owner = models.CharField(max_length=50,null=True,blank=True)
	post_indicator = models.CharField(max_length=5,null=True,blank=True)
	remark = models.CharField(max_length=100,null=True,blank=True)
	last_update_date = models.DateField(null=True,blank=True)
	mode = models.CharField(max_length=50,null=True,blank=True)
	bk_date = models.DateField()

###end of journal###

###begining of ledger###

class ledger(models.Model):

	class Meta:
		verbose_name = 'general ledger'
		ordering = ['balancesheet_type','gl_account']

	balancesheet_type = models.CharField('ledger type',max_length=50,choices=(('asset','asset'),('liability','liability'),('income','income'),('expense','expense')))
	account = models.CharField('account',max_length=50,null=True,blank=True)
	gl_account = models.CharField('GL account',max_length=50)
	activity_category = models.CharField('activity category',max_length=50,null=True,blank=True)
	activity = models.CharField('activity',max_length=50)
	amount = models.DecimalField('amount',max_digits=8,decimal_places=2)
	currency = models.CharField('currency',max_length=10)
	owner = models.CharField('owner',max_length=50)
	mode = models.CharField('mode',max_length=100,null=True,blank=True)
	remark = models.CharField('remark',max_length=100,null=True,blank=True)

	def __unicode__(self):
		return self.balancesheet_type + ' ' + self.gl_account
	
	@classmethod
	def post(self,jrnl):
		j = journal.objects.filter(journal_id=jrnl,post_indicator__isnull=True)
		
		for o in j:
			try:
				self.objects.update_or_create(gl_account = o.gl_account, account = o.account,
											balancesheet_type = o.balancesheet_type, currency = o.currency,
													 activity = o.activity, activity_category = o.activity_category,
													    owner = o.owner,
	                                                     mode = o.mode,
													 defaults = {'amount':F('amount')+o.amount})
			except:
				self.objects.create(gl_account = o.gl_account, account = o.account,
					   balancesheet_type = o.balancesheet_type, 
								  amount = o.amount, currency = o.currency,owner = o.owner,
	                                mode = o.mode,
								activity = o.activity, activity_category = o.activity_category)
				
		j.update(post_indicator='Y')
		
	@classmethod
	def get(self,attr='',user=''):
		if attr == 'checkbs':
			return self.objects.filter(owner=user,balancesheet_type='asset' or 'liability')\
			.order_by('balancesheet_type','gl_account','account','currency')\
			.values('balancesheet_type','gl_account','account','currency')\
			.annotate(amount = Sum('amount'))
		elif attr == 'checkpl':
			return self.objects.filter(owner=user)\
			.exclude(balancesheet_type='asset' or 'liability')\
			.order_by('balancesheet_type','currency')\
			.values('balancesheet_type','currency')\
			.annotate(amount = Sum('amount'))
	        
	@classmethod
	def remove_test(self):
		self.objects.filter(mode='test').delete()


class ledger_m(models.Model):
	balancesheet_type = models.CharField(max_length=50,null=True,blank=True)
	account = models.CharField(max_length=50,null=True,blank=True)
	gl_account = models.CharField(max_length=50,null=True,blank=True)
	activity_category = models.CharField(max_length=50,null=True,blank=True)
	activity = models.CharField(max_length=50,null=True,blank=True)
	amount = models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
	currency = models.CharField(max_length=10,null=True,blank=True)
	owner = models.CharField(max_length=50,null=True,blank=True)
	mode = models.CharField(max_length=100,null=True,blank=True)
	remark = models.CharField(max_length=100,null=True,blank=True)
	bk_date = models.DateField()

###end of ledger###
