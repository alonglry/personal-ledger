from __future__ import unicode_literals
import datetime
from django.db import models

# to be imported
from GL_map import *
# end of import

'''
class all_tables(models.Model):
	project = models.CharField(max_length=100,null=True,blank=True)
	model_file_name = models.CharField(max_length=200,null=True,blank=True)
	table_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name_plural = models.CharField(max_length=100,null=True,blank=True)
	ordering = models.CharField(max_length=200,null=True,blank=True)
	definition = models.CharField(max_length=200,null=True,blank=True)
	if_migrated = models.CharField(max_length=10,null=True,blank=True)
	last_update_date = models.DateTimeField(auto_now=True,null=True,blank=True)
	
class stg_all_tables(models.Model):
	action = models.CharField(max_length=10,null=True,blank=True)
	status = models.CharField(max_length=10,null=True,blank=True)
	project = models.CharField(max_length=100,null=True,blank=True)
	model_file_name = models.CharField(max_length=200,null=True,blank=True)
	table_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name_plural = models.CharField(max_length=100,null=True,blank=True)
	ordering = models.CharField(max_length=200,null=True,blank=True)
	definition = models.CharField(max_length=200,null=True,blank=True)
	last_update_date = models.DateTimeField(auto_now=True,null=True,blank=True)

class all_tab_colums(models.Model):
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
	
class stg_all_tab_colums(models.Model):
	action = models.CharField(max_length=10,null=True,blank=True)
	status = models.CharField(max_length=10,null=True,blank=True)
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
	last_update_date = models.DateTimeField(auto_now=True,null=True,blank=True)
'''

