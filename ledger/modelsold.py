from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.forms import ModelForm

# Create your models here.

balancesheet_type_choice = (
	('asset','asset'),
	('liability','liability'),
	('income','income'),
	('expense','expense'),
)

#account information
class account_info(models.Model):

	class Meta:
		verbose_name = 'account information'
		verbose_name_plural = "accounts information"
		ordering = ['company','identifier']
		
	identifier = models.CharField("account",max_length=50,unique=True)
	number = models.CharField(max_length=50)
	company = models.CharField(max_length=50)
	owner = models.CharField(default='Awai',max_length=50)
	country = models.CharField(default='Singapore',max_length=50)
	type = models.CharField(max_length=50)
	status = models.CharField(default='active',max_length=50)
	currency = models.CharField(default='SGD',max_length=10)
	amount = models.DecimalField(default='0.00',max_digits=10, decimal_places=2)
	remark = models.CharField(max_length=100,null=True,blank=True)

	def __unicode__(self):
		return self.identifier

class account_info_m(models.Model):

	class Meta:
		verbose_name = 'account information backup'
		verbose_name_plural = "accounts information backups"
		ordering = ['company','identifier']
	
	bk_date = models.DateField()
	identifier = models.CharField("account",max_length=50,unique=True)
	number = models.CharField(max_length=50,null=True,blank=True)
	company = models.CharField(max_length=50,null=True,blank=True)
	owner = models.CharField(max_length=50,null=True,blank=True)
	country = models.CharField(max_length=50,null=True,blank=True)
	type = models.CharField(max_length=50,null=True,blank=True)
	status = models.CharField(max_length=50,null=True,blank=True)
	currency = models.CharField(max_length=10,null=True,blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
	remark = models.CharField(max_length=100,null=True,blank=True)

	def __unicode__(self):
		return self.identifier

class account_infoForm(ModelForm):
	class Meta:
		model = account_info
		fields = ['identifier','number','company','owner','country','type','status','currency']
		
class investment_info(models.Model):
	
	class Meta:
		verbose_name = 'investment information'
		verbose_name_plural = 'investment information'
		ordering = ['type','identifier']
		
	identifier = models.CharField("ticker",max_length=50,unique=True)
	company = models.CharField(max_length=50,null=True,blank=True)
	country = models.CharField(max_length=50,null=True,blank=True)
	type = models.CharField(max_length=50,null=True,blank=True)
	paid_amount = models.DecimalField(default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	sold_amount = models.DecimalField(default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	last_update_amount = models.DecimalField(default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	unit = models.DecimalField(default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	current_price = models.DecimalField('current price',default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	current_amount = models.DecimalField('current amount',default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	currency = models.CharField(default='SGD',max_length=10,null=True,blank=True)
	profit_loss = models.DecimalField("profit/loss",default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	commission = models.DecimalField(default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	dividend = models.DecimalField(default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	total_profit_loss = models.DecimalField('total profit/loss',default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	total_yield = models.DecimalField('yield',default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	percentage = models.DecimalField(default=0.00,max_digits=10, decimal_places=2,null=True,blank=True)
	remark = models.CharField(max_length=100,null=True,blank=True)
	

#account month end balance
class account_me(models.Model):
	
	class Meta:
		verbose_name = 'account month-end balance'
		verbose_name_plural = "accounts month-end balance"
		ordering = ['account','date']
	
	date = models.DateField()
	account = models.ForeignKey('account_info',on_delete=models.PROTECT,to_field='identifier')
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=10)
	monthend_indicator = models.CharField(max_length=3)
	remark = models.CharField(max_length=100,null=True,blank=True)

	def __unicode__(self):
		return self.account
		
#general ledger account information
class gl_info(models.Model):

	class Meta:
		verbose_name = 'ledger account setting'
		ordering = ['balancesheet_type','asset_type','level_1_category','level_2_category','identifier']
		unique_together = (('identifier','balancesheet_type'),)

	identifier = models.CharField("GL account",max_length=50)
	balancesheet_type = models.CharField("ledger",max_length=10,choices=balancesheet_type_choice)
	asset_type = models.CharField("asset type",max_length=50,null=True,blank=True)
	asset_holder = models.CharField("asset holder",max_length=50,null=True,blank=True)
	asset_source = models.CharField("asset source",max_length=50,null=True,blank=True)
	level_1_category = models.CharField("category 1",max_length=50,null=True,blank=True)
	level_2_category = models.CharField("category 2",max_length=50,null=True,blank=True)
	remark = models.CharField(max_length=100,null=True,blank=True)

	def __unicode__(self):
		return self.identifier

class gl_infoForm(ModelForm):
	class Meta:
		model = gl_info
		fields = ['identifier','balancesheet_type','asset_type','asset_holder','asset_source','level_1_category','level_2_category']
		
class journal(models.Model):

	#class Meta:
		#ordering = ['date','reference','balancesheet_type']
		
	date = models.DateField()
	year = models.IntegerField(null=True,blank=True)
	month = models.IntegerField(null=True,blank=True)
	
	account = models.ForeignKey('account_info',on_delete=models.PROTECT,to_field='identifier',null=True,blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=10)
	#gl_account = models.ForeignKey('gl_info',on_delete=models.PROTECT,to_field='identifier')
	gl_account = models.CharField("GL account",max_length=50)
	balancesheet_type = models.CharField(max_length=10,choices=balancesheet_type_choice)
	activity = models.CharField(max_length=50)
	activity_category = models.CharField(max_length=50,null=True,blank=True)
	reference = models.CharField(max_length=100)
	journal_id = models.CharField(max_length=100,null=True,blank=True)
	last_update_date = models.DateField(auto_now=True,null=True,blank=True)
	post_indicator = models.CharField(max_length=5,null=True,blank=True)
	remark = models.CharField(max_length=100,null=True,blank=True)
	
	def __unicode__(self):
		return '%s %s' % (self.date, self.reference)

class journal_m(models.Model):

	#class Meta:
		#ordering = ['date','reference','balancesheet_type']
	
	bk_date = models.DateField()
	
	date = models.DateField(null=True,blank=True)
	year = models.IntegerField(null=True,blank=True)
	month = models.IntegerField(null=True,blank=True)
	
	account_id = models.CharField("account",max_length=50,null=True,blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	currency = models.CharField(max_length=10,null=True,blank=True)
	#gl_account = models.ForeignKey('gl_info',on_delete=models.PROTECT,to_field='identifier')
	gl_account = models.CharField("GL account",max_length=50,null=True,blank=True)
	balancesheet_type = models.CharField(max_length=10,null=True,blank=True)
	activity = models.CharField(max_length=50,null=True,blank=True)
	activity_category = models.CharField(max_length=50,null=True,blank=True)
	reference = models.CharField(max_length=100,null=True,blank=True)
	journal_id = models.CharField(max_length=100,null=True,blank=True)
	last_update_date = models.DateField(auto_now=True,null=True,blank=True)
	post_indicator = models.CharField(max_length=5,null=True,blank=True)
	remark = models.CharField(max_length=100,null=True,blank=True)
	
	def __unicode__(self):
		return '%s %s' % (self.date, self.reference)
		
class ledger(models.Model):

	class Meta:
		verbose_name = 'general ledger'
		verbose_name_plural = "general ledger"
		ordering = ['balancesheet_type','gl_account']
	
	#gl_account = models.ForeignKey('gl_info',on_delete=models.PROTECT,to_field='identifier')
	gl_account = models.CharField("GL account",max_length=50)
	account = models.ForeignKey('account_info',on_delete=models.PROTECT,to_field='identifier',null=True,blank=True)
	balancesheet_type = models.CharField("ledger type",max_length=10,choices=balancesheet_type_choice)
	activity = models.CharField(max_length=50)
	activity_category = models.CharField(max_length=50,null=True,blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=10)
	remark = models.CharField(max_length=100,null=True,blank=True)
	def __unicode__(self):
		return self.gl_account

class ledgerForm(ModelForm):
    class Meta:
        model = ledger
        fields = ['gl_account','account','balancesheet_type','activity','amount','currency']
		
class investment_transaction(models.Model):

	class Meta:
		verbose_name = 'investment transaction'
		verbose_name_plural = "investment transaction"
		ordering = ['date','identifier','transaction_type_1','transaction_type_1']
		
	date = models.DateField() 
	identifier = models.ForeignKey("investment_info",on_delete=models.PROTECT,to_field='identifier')
	transaction_type_1 = models.CharField(max_length=50)
	transaction_type_2 = models.CharField(max_length=50)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	unit = models.DecimalField(max_digits=10, decimal_places=2)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=10)
	journal_id = models.CharField(max_length=100,null=True,blank=True)
	remark = models.CharField(max_length=100,null=True,blank=True)
	
	def __unicode__(self):
		return self.identifier
		
class parameter(models.Model):
	value_1 = models.CharField("parameter",max_length=50,null=True,blank=True)
	value_2 = models.CharField("text value 1",max_length=50,null=True,blank=True)
	value_3 = models.CharField("text value 2",max_length=50,null=True,blank=True)
	value_4 = models.DecimalField("number value",max_digits=10, decimal_places=10,null=True,blank=True)
	value_5 = models.DateField("date value",null=True,blank=True,default=datetime.datetime.now().strftime("%Y-%m-%d"))
	
	def __unicode__(self):
		return self.value_1
		
class parameterForm(ModelForm):
    class Meta:
        model = parameter
        fields = ['value_1', 'value_2', 'value_3','value_4','value_5']
		
class cashflow(models.Model):
	year = models.IntegerField()
	month = models.IntegerField()
	salary = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	rental = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	phone = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	dividendcard = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	saving = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	
	def __unicode__(self):
		return str(self.year) + ' ' + str(month)

class cashflow_m(models.Model):
	bk_date = models.DateField()
	year = models.IntegerField()
	month = models.IntegerField()
	salary = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	rental = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	phone = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	dividendcard = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	saving = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
	
	def __unicode__(self):
		return str(self.year) + ' ' + str(month)