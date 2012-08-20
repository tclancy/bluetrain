from django.conf import settings
from django.core.cache import cache
from django.contrib.sites.models import Site

from bluetrain.models import HtmlPage


def base_page_variables(context):
    return {'MEDIA_URL': settings.MEDIA_URL}


def site_name(context):
    return {'current_site_name': Site.objects.get_current().name}


def site_home_page(context):
    cache_key = 'site_home_page'
    home = cache.get(cache_key)
    if not home:
        try:
            home = HtmlPage.objects.get(slug='home')
            if settings.USE_CACHE:
                cache.set(cache_key, home, settings.DEFAULT_CACHE_TIMEOUT)
        except HtmlPage.DoesNotExist:
            pass
    return {'home_page': home}
