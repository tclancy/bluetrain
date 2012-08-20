from django.conf.urls.defaults import *


urlpatterns = patterns('bluetrain.views',
    url(r'^sitemap/?$', 'sitemap', name='sitemap'),
    url(r'^thank-you/(?P<form_slug>[^/]+)/?$', 'form_thank_you', name='form_thank_you'),
    url(r'^contact-us/?$', 'show_page', {'slug': 'contact-us'}, name="pages_contact_us"),
    (r'^404?$', 'show_page', {'slug': 'home', 'template': 'pages/404.html'}),
    (r'^500?$', 'show_page', {'slug': 'home', 'template': 'pages/500.html'}),
    url(r'^(.*/)?(?P<slug>[^/]+)/?$', 'show_page', name='pages_display'),
)
