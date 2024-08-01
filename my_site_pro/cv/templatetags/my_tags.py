from django import template
from django.template.defaultfilters import stringfilter
from django.http import QueryDict


register = template.Library()



@register.filter
@stringfilter
def replace(value, args):
    qs = QueryDict(args)
    return value.replace(qs.get('old',''), qs.get('new',''))

