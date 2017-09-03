from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from ..forms import login_form

def login_handler(request):
	if request.META.get('HTTP_USER_AGENT', '').lower().find("iphone") > 0:
		device = 'phone'
	else:
		device = 'others'
		
	current_path = "http://alonglry.pythonanywhere.com"+request.get_full_path()
		
	if request.method == 'POST':
		username = request.POST.get('user','')
		password = request.POST.get('password','')
		next_page = request.POST.get('next_page','').replace('next=%2F','').replace('%2F','')
		user = authenticate(username=username, password=password)
		#return HttpResponse(user)
		if user is not None:
			if user.is_active:
				login(request, user)
				# Redirect to a success page.
				if next_page <> '':
					#return HttpResponse(next_page)
					return HttpResponseRedirect(reverse('ledger:%s' % next_page))
				else:
					return HttpResponseRedirect(reverse('ledger:accounts'))
			else:
				# Return a 'disabled account' error message
				return render(request,'ledger/login.html',{'login':login_form(),
				                                           'device':device,
														   'current_path':current_path,
														   'error':'disabled account'})
		else:
			# Return an 'invalid login' error message.
			return render(request,'ledger/login.html',{'login':login_form(),
			                                           'device':device,
													   'current_path':current_path,
													   'error':'wrong password'})
	else:
		return render(request,'ledger/login.html',{'login':login_form(),
		                                           'device':device,
												   'current_path':current_path})

def logout_handler(request):
	logout(request)
	return HttpResponseRedirect(reverse('ledger:login'))