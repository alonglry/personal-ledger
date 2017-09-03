import datetime
from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F,Sum,Avg,Max,Min

###begining of sql###

class sql(models.Model):

	class Meta:
		verbose_name = 'sql'

	sql = models.CharField('sql',max_length=500)

	def __unicode__(self):
		return str(self.id) + ' - ' + self.sql



###end of sql###

###begining of parameter###

class parameter(models.Model):

	class Meta:
		verbose_name = 'parameter'

	value_1 = models.CharField('parameter',max_length=50)
	value_2 = models.CharField('text value',max_length=100,null=True,blank=True)
	value_3 = models.CharField('text value',max_length=100,null=True,blank=True)
	value_4 = models.DecimalField('number value',max_digits=8,decimal_places=2,null=True,blank=True)
	value_5 = models.DateField('date value',null=True,blank=True)

	def __unicode__(self):
		return self.value_1
	
	@classmethod
	def get(self,value1='',value2='',value3=''):
		if value1 == 'basic expense':
			a = self.objects.get(value_1='basic expense',value_2=value2).value_3.split(',')
			return a
	    
	@classmethod
	def mode(self):
		return self.objects.get(value_1='mode').value_2


class parameter_m(models.Model):
	value_1 = models.CharField(max_length=50,null=True,blank=True)
	value_2 = models.CharField(max_length=100,null=True,blank=True)
	value_3 = models.CharField(max_length=100,null=True,blank=True)
	value_4 = models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
	value_5 = models.DateField(null=True,blank=True)
	bk_date = models.DateField()

###end of parameter###

###begining of all_tables###

class all_tables(models.Model):

	class Meta:
		verbose_name = 'all tables'
		ordering = ['project','model_file_name','table_name']

	project = models.CharField('project',max_length=100,null=True,blank=True)
	model_file_name = models.CharField('model file name',max_length=200,null=True,blank=True)
	table_name = models.CharField('table name',max_length=100,null=True,blank=True)
	verbose_name = models.CharField('verbose name',max_length=100,null=True,blank=True)
	verbose_name_plural = models.CharField('verbose name plural',max_length=100,null=True,blank=True)
	ordering = models.CharField('ordering',max_length=200,null=True,blank=True)
	definition = models.CharField('definition',max_length=200,null=True,blank=True)
	if_migrated = models.CharField('if migrated',max_length=10,null=True,blank=True)
	last_update_date = models.DateTimeField('last update_date',auto_now=True,null=True,blank=True)
	remark = models.CharField('remark',max_length=200,null=True,blank=True)
	model_form = models.CharField('model form',max_length=10,null=True,blank=True)
	backup = models.CharField('backup',max_length=10,null=True,blank=True)
	unicode = models.CharField('unicode',max_length=200,null=True,blank=True)
	retention_d = models.IntegerField('retention days',null=True,blank=True)
	status = models.CharField('status',max_length=10,null=True,blank=True)

	def __unicode__(self):
		return self.project + ' ' + self.model_file_name + ' ' + self.table_name
	
	@classmethod
	def update(self,i,c,v):
		obj = self.objects.get(id=i)
		obj.__dict__.update({c:v})
		obj.save()
			
	@classmethod
	def add(self,p=None,f=None,t=None,v=None,vp=None,o=None,d=None,m=None,b=None,u=None,r=None):
		obj = self.objects.create(project=p,model_file_name=f,table_name=t,verbose_name=v,verbose_name_plural=vp,ordering=o,definition=d,model_form=m,backup=b,unicode=u,retention_d=n(r))
		return obj
			
	@classmethod
	def get(self,attr=''):
		if attr == 'pm':
			return self.objects.order_by('project','model_file_name').values('project','model_file_name').distinct()
	
	def n(value=None):
		return None if value == '' else value

class all_tables_form(ModelForm):
	class Meta:
		model = all_tables
		fields = ['project','model_file_name','table_name','verbose_name','verbose_name_plural','ordering','definition','if_migrated','remark','model_form','backup','retention_d','status']

class all_tables_m(models.Model):
	project = models.CharField(max_length=100,null=True,blank=True)
	model_file_name = models.CharField(max_length=200,null=True,blank=True)
	table_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name_plural = models.CharField(max_length=100,null=True,blank=True)
	ordering = models.CharField(max_length=200,null=True,blank=True)
	definition = models.CharField(max_length=200,null=True,blank=True)
	if_migrated = models.CharField(max_length=10,null=True,blank=True)
	last_update_date = models.DateTimeField(null=True,blank=True)
	remark = models.CharField(max_length=200,null=True,blank=True)
	model_form = models.CharField(max_length=10,null=True,blank=True)
	backup = models.CharField(max_length=10,null=True,blank=True)
	unicode = models.CharField(max_length=200,null=True,blank=True)
	retention_d = models.IntegerField(null=True,blank=True)
	status = models.CharField(max_length=10,null=True,blank=True)
	bk_date = models.DateField()

###end of all_tables###

###begining of all_table_columns###

class all_table_columns(models.Model):

	class Meta:
		verbose_name = 'all table column'
		verbose_name_plural = 'all table columns'
		ordering = ['project','model_file_name','table_name','sn','column_name']

	project = models.CharField('project',max_length=100,null=True,blank=True)
	model_file_name = models.CharField('model file name',max_length=100,null=True,blank=True)
	table_name = models.CharField('table name',max_length=100,null=True,blank=True)
	column_name = models.CharField('column name',max_length=100,null=True,blank=True)
	sn = models.IntegerField('serial number',validators=[MinValueValidator(0),MaxValueValidator(999)],null=True,blank=True)
	verbose_name = models.CharField('verbose name',max_length=100,null=True,blank=True)
	verbose_name_plural = models.CharField('verbose name plural',max_length=100,null=True,blank=True)
	definition = models.CharField('definition',max_length=500,null=True,blank=True)
	data_type = models.CharField('data type',max_length=100,null=True,blank=True)
	decimal_place = models.CharField('decimal place',max_length=100,null=True,blank=True)
	min_length = models.CharField('min length',max_length=10,null=True,blank=True)
	max_length = models.CharField('max length',max_length=10,null=True,blank=True)
	default_value = models.CharField('default value',max_length=100,null=True,blank=True)
	choice_options = models.CharField('choice options',max_length=500,null=True,blank=True)
	unique_key = models.CharField('unique key',max_length=10,null=True,blank=True)
	blank = models.CharField('blank',max_length=10,null=True,blank=True)
	nullable = models.CharField('nullable',max_length=10,null=True,blank=True)
	model_form = models.CharField('model form',max_length=100,null=True,blank=True)
	path = models.CharField('path',max_length=50,null=True,blank=True)
	foreign_key_table = models.CharField('foreign key table',max_length=200,null=True,blank=True)
	foreign_key_column = models.CharField('foreign key_column',max_length=200,null=True,blank=True)
	foreign_key_on_delete = models.CharField('foreign key on delete',max_length=10,null=True,blank=True)
	auto_save_foreign_key = models.CharField('auto save foreign key',max_length=10,null=True,blank=True)
	if_migrated = models.CharField('if migrated',max_length=10,null=True,blank=True)
	remark = models.CharField('remark',max_length=500,null=True,blank=True)
	last_update_date = models.DateTimeField('last update date',auto_now=True,null=True,blank=True)

	def __unicode__(self):
		return self.project + ' ' + self.model_file_name + ' ' + self.table_name + ' ' + self.column_name
	
	@classmethod
	def update(self,i,c,v):
		obj = self.objects.get(id=i)
		obj.__dict__.update({c:v})
		obj.save()
			
	@classmethod
	def add(self,pj=None,mfn=None,tn=None,s=None,c=None,v=None,vp=None,d=None,dv=None,co=None,dt=None,mil=None,mal=None,dp=None,p=None,n=None,b=None,uk=None,mf=None,fkt=None,fkc=None,fkod=None,asfk=None):
		s = int(s) if s <> '' else None
		obj = self.objects.create(project=pj,model_file_name=mfn,table_name=tn,sn=s,column_name=c,verbose_name=v,verbose_name_plural=vp,data_type=dt,min_length=mil,max_length=mal,definition=d,choice_options=co,foreign_key_table=fkt,foreign_key_column=fkc,foreign_key_on_delete=fkod,nullable=n,blank=b,unique_key=uk,default_value=dv,auto_save_foreign_key=asfk,decimal_place=dp,model_form=mf,path=p)
		return obj

class all_table_columns_form(ModelForm):
	class Meta:
		model = all_table_columns
		fields = ['project','model_file_name','table_name','column_name','sn','verbose_name','verbose_name_plural','definition','data_type','decimal_place','min_length','max_length','default_value','choice_options','unique_key','blank','nullable','model_form','path','foreign_key_table','foreign_key_column','foreign_key_on_delete','auto_save_foreign_key','if_migrated','remark']

class all_table_columns_m(models.Model):
	project = models.CharField(max_length=100,null=True,blank=True)
	model_file_name = models.CharField(max_length=100,null=True,blank=True)
	table_name = models.CharField(max_length=100,null=True,blank=True)
	column_name = models.CharField(max_length=100,null=True,blank=True)
	sn = models.IntegerField(null=True,blank=True)
	verbose_name = models.CharField(max_length=100,null=True,blank=True)
	verbose_name_plural = models.CharField(max_length=100,null=True,blank=True)
	definition = models.CharField(max_length=500,null=True,blank=True)
	data_type = models.CharField(max_length=100,null=True,blank=True)
	decimal_place = models.CharField(max_length=100,null=True,blank=True)
	min_length = models.CharField(max_length=10,null=True,blank=True)
	max_length = models.CharField(max_length=10,null=True,blank=True)
	default_value = models.CharField(max_length=100,null=True,blank=True)
	choice_options = models.CharField(max_length=500,null=True,blank=True)
	unique_key = models.CharField(max_length=10,null=True,blank=True)
	blank = models.CharField(max_length=10,null=True,blank=True)
	nullable = models.CharField(max_length=10,null=True,blank=True)
	model_form = models.CharField(max_length=100,null=True,blank=True)
	path = models.CharField(max_length=50,null=True,blank=True)
	foreign_key_table = models.CharField(max_length=200,null=True,blank=True)
	foreign_key_column = models.CharField(max_length=200,null=True,blank=True)
	foreign_key_on_delete = models.CharField(max_length=10,null=True,blank=True)
	auto_save_foreign_key = models.CharField(max_length=10,null=True,blank=True)
	if_migrated = models.CharField(max_length=10,null=True,blank=True)
	remark = models.CharField(max_length=500,null=True,blank=True)
	last_update_date = models.DateTimeField(null=True,blank=True)
	bk_date = models.DateField()

###end of all_table_columns###

###begining of all_table_functions###

class all_table_functions(models.Model):

	project = models.CharField('projec',max_length=100,null=True,blank=True)
	model_file_name = models.CharField('model file name',max_length=100,null=True,blank=True)
	table_name = models.CharField('table name',max_length=100,null=True,blank=True)
	function = models.CharField('function',max_length=999999,null=True,blank=True)

	@classmethod
	def add(self,p=None,f=None,t=None,v=None):
		obj = self.objects.create(project=p,model_file_name=f,table_name=t,function=v)
		return obj
			
	@classmethod
	def update(self,i,v):
		obj = self.objects.get(id=i)
		obj.function = v
		obj.save()


class all_table_functions_m(models.Model):
	project = models.CharField(max_length=100,null=True,blank=True)
	model_file_name = models.CharField(max_length=100,null=True,blank=True)
	table_name = models.CharField(max_length=100,null=True,blank=True)
	function = models.CharField(max_length=999999,null=True,blank=True)
	bk_date = models.DateField()

###end of all_table_functions###
