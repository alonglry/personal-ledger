from django import forms
import datetime

class sql_form(forms.Form):
	input = forms.CharField(widget=forms.Textarea)
	
class transaction_form(forms.Form):
	input = forms.CharField(widget=forms.Textarea)
	
'''	
class basic_journal_form(forms.Form):
	journal_activities = (
	('salary','salary'),
	('rental','rental'),
	('4G','4G'),
	('Citi dividend','Dividend Card')
	)
	date = forms.DateField(initial=datetime.datetime.now().strftime("%Y-%m-%d"))
	#choice = forms.ChoiceField(choices = journal_activities,label='activities')
	choice = forms.CharField(max_length=50,required = False)
	amount = forms.DecimalField(max_digits=10, decimal_places=2)
	#initial=datetime.date time.now().strftime("%Y-%m-%d"),

class trip_form(forms.Form):
	date = forms.DateField(initial=datetime.datetime.now().strftime("%Y-%m-%d"))
	amount = forms.DecimalField(max_digits=10, decimal_places=2)
'''
class vickers_journal_form(forms.Form):
	vickers_activities = (
	('transfer','transfer'),
	('buy','buy'),
	('sell','sell'),
	('dividend','dividend'),
	('mtm','mtm')
	)
	date = forms.DateField(initial=datetime.datetime.now().strftime("%Y-%m-%d"))
	choice =  forms.ChoiceField(choices = vickers_activities,label='activities')
	ticker = forms.CharField(max_length=10,required = False)
	unit = forms.IntegerField(required = False)
	price = forms.DecimalField(max_digits=10, decimal_places=2,required = False)
'''
class fundsupermart_journal_form(forms.Form):
	vickers_activities = (
	('buy','buy'),
	('sell','sell'),
	('commission','commission'),
	)
	date = forms.DateField(initial=datetime.datetime.now().strftime("%Y-%m-%d"))
	choice =  forms.ChoiceField(choices = vickers_activities,label='activities')
	fund = forms.CharField(max_length=10)
	unit = forms.DecimalField(max_digits=10, decimal_places=2)
	amount = forms.DecimalField(max_digits=10, decimal_places=2)
	
class dbs_sos_journal_form(forms.Form):
	dbs_sos_activities = (
	('buy','buy'),
	('sell','sell'),
	('dividend','dividend'),
	)
	date = forms.DateField(initial=datetime.datetime.now().strftime("%Y-%m-%d"))
	choice =  forms.ChoiceField(choices = dbs_sos_activities,label='activities')
	unit = forms.DecimalField(max_digits=10, decimal_places=2,required = False)
	amount = forms.DecimalField(initial=615, max_digits=10, decimal_places=2,required = False)

class cpf_journal_form(forms.Form):
	date = forms.DateField(initial=datetime.datetime.now().strftime("%Y-%m-%d"))
	ordinary = forms.DecimalField(initial=953.69, max_digits=10, decimal_places=2,required = False)
	special = forms.DecimalField(initial=248.66, max_digits=10, decimal_places=2,required = False)
	medisave = forms.DecimalField(initial=331.65, max_digits=10, decimal_places=2,required = False)
	medishield = forms.DecimalField(max_digits=10, decimal_places=2,required = False)
	dps = forms.DecimalField(max_digits=10, decimal_places=2,required = False)
'''
class journal_form(forms.Form):
	balancesheet_type_choice = (
	('asset','asset'),
	('liability','liability'),
	('income','income'),
	('expense','expense'),
	)
	date = forms.DateField(initial=datetime.datetime.now().strftime("%Y-%m-%d"))
	amount = forms.DecimalField(max_digits=10, decimal_places=2)
	currency = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder': 'currency'}))
	balancesheet_type_1 = forms.ChoiceField(choices=balancesheet_type_choice)
	balancesheet_type_2 = forms.ChoiceField(choices=balancesheet_type_choice,required = False)
	activity = forms.CharField(max_length=50)
	activity_category = forms.CharField(max_length=50,required = False,widget=forms.TextInput(attrs={'placeholder': 'activity category'}))
	reference = forms.CharField(max_length=100,required = False)
	account_id_1 = forms.CharField(max_length=50,required = False)
	gl_account_1 = forms.CharField(max_length=50)
	account_id_2 = forms.CharField(max_length=50,required = False)
	gl_account_2 = forms.CharField(max_length=50,required = False)
	journal_id = forms.CharField(max_length=100,required = False,widget=forms.TextInput(attrs={'placeholder': 'journal ID'}))
	
class login_form(forms.Form):
	user = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'xqq or xgg'}))
	#user = forms.ChoiceField(widget=forms.RadioSelect, choices=(('xqq', 'xqq',), ('xgg', 'xgg',)))
	password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	