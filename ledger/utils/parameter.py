from ..models import parameter

def ledger_posting():
	tmp = True
	if parameter.objects.get(value_1='ledger mode').value_2 == 'N':
		tmp = False
	return tmp	