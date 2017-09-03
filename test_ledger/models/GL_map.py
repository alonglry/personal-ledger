import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator

###begining of map_bu###
class map_bu(models.Model):

	class Meta:
		verbose_name = 'Business Unit'
		verbose_name_plural = 'Business Units'
		ordering = ['bu']

	bu = models.CharField('business unit',max_length=20,unique=True)
	descr = models.CharField('description',max_length=200,null=True,blank=True)

	def __unicode__(self):
		return self.bu

###end of map_bu###
###end of map_bu customised###

###begining of map_ledger###
class map_ledger(models.Model):

	class Meta:
		verbose_name = 'Ledger Book'
		verbose_name_plural = 'Ledger Books'
		ordering = ['ledger']

	descr = models.CharField('description',max_length=200,null=True,blank=True)
	ledger = models.CharField('ledger',max_length=20,unique=True)
	lvl1_cat = models.CharField('level 1 category',max_length=200,null=True,blank=True)
	lvl2_cat = models.CharField('level 2 category',max_length=200,null=True,blank=True)
	lvl3_cat = models.CharField('level 3 category',max_length=200,null=True,blank=True)
	lvl4_cat = models.CharField('level 4 category',max_length=200,null=True,blank=True)
	lvl5_cat = models.CharField('level 5 category',max_length=200,null=True,blank=True)

	def __unicode__(self):
		return self.ledger

###end of map_ledger###
###end of map_ledger customised###

###begining of map_acct_rollup###
class map_acct_rollup(models.Model):

	class Meta:
		verbose_name = 'GL account list'
		verbose_name_plural = 'GL account list'
		ordering = ['acct']

	acct = models.IntegerField('GL account',validators=[MinValueValidator(10000),MaxValueValidator(99999)],unique=True)
	acct_owner = models.CharField('account owner',max_length=100,null=True,blank=True)
	bu = models.ForeignKey('map_bu',to_field='bu',on_delete=models.PROTECT,verbose_name='business unit')
	descr = models.CharField('description',max_length=200,null=True,blank=True)
	ledger = models.ForeignKey('map_ledger',to_field='ledger',on_delete=models.PROTECT,verbose_name='ledger')
	lu_date = models.DateField('last update date',auto_now=True,null=True,blank=True)
	lu_user = models.CharField('last update user',max_length=50,null=True,blank=True)
	lvl2_cat = models.CharField('level 2 category',max_length=100,null=True,blank=True)
	lvl3_cat = models.CharField('level 3 category',max_length=100,null=True,blank=True)
	lvl4_cat = models.CharField('level 4 category',max_length=100,null=True,blank=True)
	purpose = models.CharField('purpose',max_length=200,null=True,blank=True)
	statement = models.CharField('financial statement',max_length=100,null=True,blank=True,choices=(('balancesheet','balancesheet'),('income statement','income statement')))

	def __unicode__(self):
		return self.acct

###end of map_acct_rollup###
###end of map_acct_rollup customised###

###begining of map_acct_rollup_form###
class map_acct_rollup_form(ModelForm):
	class Meta:
		model = map_acct_rollup
		fields = ['acct','acct_owner','bu','descr','ledger','lvl2_cat','lvl3_cat','lvl4_cat','purpose','statement']
###end of map_acct_rollup_form###
###end of map_acct_rollup_form customised###

