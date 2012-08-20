from django import template
from django.conf import settings
from django.template import Context, Template, TemplateDoesNotExist
from django.template.loader import get_template

register = template.Library()

try:
    FORM_TEMPLATE = settings.BLUETRAIN_DEFAULT_FORM
except AttributeError:
    FORM_TEMPLATE = 'bluetrain/default_form.html'


@register.filter
def as_default_form(form):
    try:
        template = get_template(FORM_TEMPLATE)
        c = Context({'form': form})
        return template.render(c)
    except TemplateDoesNotExist:
        raise Exception('Either set BLUETRAIN_DEFAULT_FORM in settings or provide a file at %s' % FORM_TEMPLATE)
