from django import template

register = template.Library()

@register.filter
def get_type(field):
    print (type(field))
    return field.__class__.__name__

@register.filter
def get_count(field):
    return len(field)