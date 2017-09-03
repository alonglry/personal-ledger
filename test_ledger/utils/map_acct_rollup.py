import sys
from test_ledger.models import map_acct_rollup,map_acct_rollup_form

def get_acct_rollup(attr = ''):
	if attr == 'all':
		return map_acct_rollup.objects.all()
	elif attr == 'meta':
		return map_acct_rollup._meta
	elif attr == 'form':
		return map_acct_rollup_form()

def save_acct_rollup(request):
	
	try:
		if map_acct_rollup_form(request.POST).is_valid():
			map_acct_rollup(acct       = getValue(request,'acct'),
							bu_id      = getValue(request,'bu'),
							ledger_id  = getValue(request,'ledger'),
							descr      = getValue(request,'descr'),
							lvl1_cat   = getValue(request,'lvl1_cat'),
							lvl2_cat   = getValue(request,'lvl2_cat'),
							lvl3_cat   = getValue(request,'lvl3_cat'),
							lvl4_cat   = getValue(request,'lvl4_cat'),
							acct_owner = getValue(request,'acct_ownor')).save()
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		return exc_type.__name__.replace('Error',' Error') + ': ' + exc_value.message
	
def getValue(request,field):
	tmp = None if request.POST.get(field,'') == '' else request.POST.get(field,'')
	return tmp