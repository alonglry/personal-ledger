from django.http import HttpResponse
from coa import coa_handler

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. test_ledger new")
	
def coa(request):
	return coa_handler(request)