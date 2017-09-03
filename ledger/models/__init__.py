from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.forms import ModelForm

# to be imported
from ema import *
from others import *
from simulation import *
from stock import *
from sats import *
from GL import *
from account import *
# end of import

'''
class all_tables(models.Model):
	class Meta:
		ordering = ['project','model_file_name','table_name']
		
	project = models.CharField(max_length=100,null=True,blank=True)
	model_file_name = models.CharField(max_length=200,null=True,blank=True)
	table_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name_plural = models.CharField(max_length=100,null=True,blank=True)
	ordering = models.CharField(max_length=200,null=True,blank=True)
	definition = models.CharField(max_length=200,null=True,blank=True)
	if_migrated = models.CharField(max_length=10,null=True,blank=True)
	last_update_date = models.DateTimeField(auto_now=True,null=True,blank=True)
	remark = models.CharField(max_length=200,null=True,blank=True)
	model_form = models.CharField(max_length=100,null=True,blank=True)
	backup = models.CharField(max_length=10,null=True,blank=True)
	unicode = models.CharField(max_length=200,null=True,blank=True)
	retention_d = models.IntegerField(null=True,blank=True)
	status = models.CharField(max_length=10,null=True,blank=True)
	
	@classmethod
	def update(self,i,c,v):
		obj = self.objects.get(id=i)
		obj.__dict__.update({c:v})
		obj.save()
	

class all_table_columns(models.Model):
	class Meta:
		ordering = ['project','model_file_name','table_name','column_name']
	
	project = models.CharField(max_length=100,null=True,blank=True)
	model_file_name = models.CharField(max_length=200,null=True,blank=True)
	table_name = models.CharField(max_length=100,null=True,blank=True)
	column_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name_plural = models.CharField(max_length=100,null=True,blank=True)
	data_type = models.CharField(max_length=100,null=True,blank=True)
	min_length = models.CharField(max_length=100,null=True,blank=True)
	max_length = models.CharField(max_length=100,null=True,blank=True)
	definition = models.CharField(max_length=200,null=True,blank=True)
	choice_options = models.CharField(max_length=500,null=True,blank=True)
	foreign_key_table = models.CharField(max_length=200,null=True,blank=True)
	foreign_key_column = models.CharField(max_length=200,null=True,blank=True)
	foreign_key_on_delete = models.CharField(max_length=10,null=True,blank=True)
	nullable = models.CharField(max_length=10,null=True,blank=True)
	blank = models.CharField(max_length=10,null=True,blank=True)
	unique_key = models.CharField(max_length=10,null=True,blank=True)
	remark = models.CharField(max_length=200,null=True,blank=True)
	if_migrated = models.CharField(max_length=10,null=True,blank=True)
	last_update_date = models.DateTimeField(auto_now=True,null=True,blank=True)
	default_value = models.CharField(max_length=100,null=True,blank=True)
	auto_save_foreign_key = models.CharField(max_length=10,null=True,blank=True)
	decimal_place = models.CharField(max_length=100,null=True,blank=True)
	model_form = models.CharField(max_length=100,null=True,blank=True)
	path = models.CharField(max_length=500,null=True,blank=True)
	
	@classmethod
	def update(self,i,c,v):
		obj = self.objects.get(id=i)
		obj.__dict__.update({c:v})
		obj.save()
'''