from django import template
register = template.Library()

@register.simple_tag
def get_verbose(instance, field_name):
    return instance.get_field(field_name).verbose_name