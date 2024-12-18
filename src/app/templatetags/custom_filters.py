from django import template

register = template.Library()

@register.filter
def extract_last_segment(value):
    if value:
        return value.rstrip('/').split('/')[-1]
    return ''
