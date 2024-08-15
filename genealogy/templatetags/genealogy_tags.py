from django import template
from django.template.defaultfilters import stringfilter
from django.http import QueryDict
from django.template.defaulttags import register

# register = template.Library()



@register.filter
@stringfilter
def replace(value, args):
    qs = QueryDict(args)
    return value.replace(qs.get('old',''), qs.get('new',''))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)



