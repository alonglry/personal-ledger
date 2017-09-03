from django import template
register = template.Library()
from django.utils.safestring import mark_safe

@register.filter
def removenone(value):
	if value == None:
		return ''
	else:
		return value
		
@register.filter
def removeslash(value):
	return value.replace('/','')
		
@register.filter
def icon(value):
	if value in ('Citi','Amex','DBS','HSBC'):
		return mark_safe(' <i class="fa fa-credit-card" aria-hidden="true"></i>')
	else:
		return ''
		
@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})
	
@register.filter(name='addid')
def addid(value, arg):
    return value.as_widget(attrs={'id': arg})
	
@register.filter
def icon(value):
	if value in ('Citi','Amex','DBS','HSBC'):
		return mark_safe(' <i class="fa fa-credit-card" aria-hidden="true"></i>')
	elif value in ('trip'):
		return mark_safe(' <i class="fa fa-plane" aria-hidden="true"></i>')
	elif value in ('4G'):
		return mark_safe(' <i class="fa fa-mobile" aria-hidden="true"></i>')
	else:
		return ''