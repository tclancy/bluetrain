from django import template
from django.conf import settings
from django.template import Context, Template
from django.template.loader import get_template

register = template.Library()

@register.filter
def as_default_form(form):
    template = get_template('pages/default_form.html')
    c = Context({'form':form})
    return template.render(c)