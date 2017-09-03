from django import template
register = template.Library()

@register.filter
def div(value, arg):
	return float(value) / float(arg)

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return None
	
@register.filter
def percentage(value, arg):
    # you would need to do any localization of the result here
    return round(float(value) / float(arg) * 100,2)
	
@register.filter
def integer(value):
    # you would need to do any localization of the result here
	if int(value) == value:
		return int(value)
	else:
		return value
		
@register.simple_tag
def compare(j,l):
	if j == l:
		return 'ok'
	else:
		return 'x'
		
@register.assignment_tag
def define(val=None):
  return val