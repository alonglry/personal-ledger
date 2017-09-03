from ..models import sql
from django.db.models import Max

def sql_save(script):
	#script = script.strip()
	sql.objects.update_or_create(sql=script.strip())
	#sql.objects.get(sql=script).delete()
	#sql.objects.create(sql=script).save()
	a = sql.objects.aggregate(Max('id'))['id__max']
	num = max(a-10,1)
	sql.objects.filter(id__lt = num).delete()
	
def sql_get():
	return sql.objects.order_by('id')
	
def sql_truncate():
	sql.objects.all().delete()