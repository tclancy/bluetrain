from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect

from bluetrain.models import HtmlPage


def error_404(request):
    page = HtmlPage.objects.get(slug='home')
    home = False
    MEDIA_URL = settings.MEDIA_URL

    return render_to_response('404.html', locals())


def show_page(request, slug="home", template='bluetrain/page.html', extra_context={}):
    # look for cached copy of page
    if settings.USE_CACHE:
        cache_key = HtmlPage.get_cache_key_for_page(slug)
        page_view = cache.get(cache_key, None)
        if page_view:
            return page_view

    page = get_object_or_404(HtmlPage, slug=slug, active=True)

    home = False
    show_login_focus = False
    level_one = page.level_one
    is_level_one = (page == page.level_one)

    if slug == 'home':
        home = True
        template = 'bluetrain/home.html'
        level_one_class = 'Home'
    else:
        level_one_class = level_one.css_class()

    context = locals()
    context.update(extra_context)
    page_view = render_to_response(template, context, context_instance=RequestContext(request))
    if settings.USE_CACHE:
        cache.set(cache_key, page_view, settings.DEFAULT_CACHE_TIMEOUT)
    return page_view


def form_thank_you(request, form_slug):
    page = get_object_or_404(HtmlPage, slug=form_slug)

    home = False
    level_one = page.level_one
    is_level_one = (page == page.level_one)

    return render_to_response('bluetrain/form-thank-you.html', locals(), context_instance=RequestContext(request))


def sitemap(request):
    if settings.USE_CACHE:
        cache_key = 'sitemap-view'
        page_view = cache.get(cache_key, None)
        if page_view:
            return page_view
    page = HtmlPage.objects.get(slug='home')
    page_view = render_to_response('bluetrain/sitemap.html', {'page': page}, context_instance=RequestContext(request))
    if settings.USE_CACHE:
        cache.set(cache_key, page_view, settings.DEFAULT_CACHE_TIMEOUT)
    return page_view
