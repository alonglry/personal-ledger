from django import template
register = template.Library()
from django.utils.safestring import mark_safe

@register.filter
def icon(value):
	if value in ('Citi','Amex','DBS','HSBC'):
		return mark_safe(' <i class="fa fa-credit-card" aria-hidden="true"></i>')
	else:
		return ''