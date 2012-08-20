from os.path import splitext

from django.conf import settings
from django.core.cache import cache
from django.db import models, IntegrityError
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify


class PageType(models.Model):
    # constants based on data in fixture - using redundant PAGE in names
    # so I don't have a "constant" called "CONSTANT"
    HOMEPAGE = 1
    CONSTANT_PAGE = 2
    NORMAL_PAGE = 3

    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class FocusArea(models.Model):
    name = models.CharField(max_length=30, unique=True)
    link = models.ForeignKey('HtmlPage', null=True, blank=True)
    external_link = models.URLField(blank=True, verify_exists=False)
    image = models.ImageField(upload_to='img/focus-areas', blank=True)
    content = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return self.name

    def url(self):
        if self.link:
            return self.link.get_absolute_url()
        if self.external_link:
            return self.external_link
        return '#'

    class Meta:
        verbose_name = 'Focus Area'
        verbose_name_plural = 'Focus Areas'


class PageImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='img/focus-areas')

    def __unicode__(self):
        return self.name


try:
    IMAGE_ALIGNMENT_CHOICES = settings.IMAGE_ALIGNMENT_CHOICES
except AttributeError:
    IMAGE_ALIGNMENT_CHOICES = (
            ('L', 'Left'),
            ('R', 'Right'),
            ('T', 'Top'),
            ('B', 'Bottom'),
    )

class PageImageCollection(models.Model):
    image = models.ForeignKey(PageImage)
    page = models.ForeignKey('HtmlPage')
    alignment = models.CharField(max_length=1, choices=IMAGE_ALIGNMENT_CHOICES)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class LivePageManager(models.Manager):
    def get_query_set(self):
        return super(LivePageManager, self).get_query_set().filter(active=True)


class HtmlPage(models.Model):
    _children = None
    _lineage = None

    title = models.CharField(max_length=100, verbose_name='Page Title')
    title_tag = models.CharField(max_length=200, blank=True)
    keywords = models.CharField(max_length=250, blank=True)
    meta_description = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(unique=True, verbose_name='Page URL')
    content = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    page_type = models.ForeignKey(PageType)
    sort_order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    focus_areas = models.ManyToManyField(FocusArea, null=True, blank=True)

    objects = models.Manager()
    live = LivePageManager()

    def is_normal_page(self):
        return self.page_type.id == PageType.NORMAL_PAGE

    def get_images(self):
        images = []
        # cheating here: looping over the collection to get the images from it
        # but then applying the alignment in the collection's info to the img
        for img in PageImageCollection.objects.filter(page=self):
            img.image.alignment = img.alignment
            images.append(img.image)
        return images
    images = property(get_images)

    def save(self):
        if not self.id and not self.slug:
            from django.template.defaultfilters import slugify
            if self.slug == '':
                self.slug = slugify(self.title)
            try:
                existing = HtmlPage.objects.get(slug=self.slug)
                if self.parent:
                    self.slug = '%s-%s' % (self.parent.slug, self.slug)
                else:
                    self.slug = '%s-%s' % ('home', self.slug)
            except HtmlPage.DoesNotExist:
                pass
        super(HtmlPage, self).save()

    # Breadcrumb & hierarchy
    def constants(self):
        return HtmlPage.get_constants().order_by('-sort_order')

    def child_pages(self):
        if self._children:
            return self._children
        self._children = HtmlPage.get_child_pages(self.id)
        return self._children

    def lineage(self):
        crumbs = self.breadcrumbs()
        crumbs.reverse()
        # remove Home
        if len(crumbs) > 0:
            crumbs.pop()
        return crumbs

    def breadcrumbs(self):
        if self._lineage is not None:
            return self._lineage
        if self.parent is None:
            self._lineage = []
            return self._lineage

        crumbs = [self]
        dad = HtmlPage.objects.get(id=self.parent.id)
        while dad is not None:
            crumbs.append(dad)
            if dad.parent is None:
                break
            dad = HtmlPage.objects.get(id=dad.parent.id)
        crumbs.reverse()
        self._lineage = crumbs
        return self._lineage

    def get_level_one(self):
        dad = self
        if dad.parent is None:
            return self
        while dad.parent.parent is not None and dad.parent != dad.parent.parent:
            dad = dad.parent
        return dad
    level_one = property(get_level_one)

    def css_class(self):
        '''Strips a couple of common items, turns spaces into dashes and
        lower-cases to make CSS-friendly identifiers. TODO: Should really
        use a regex to knock out all alphanumeric stuff.'''
        return slugify(self.title)

    def sitemap(self):
        return HtmlPage.get_sitemap()

    @property
    def cache_key(self):
        return HtmlPage.get_cache_key_for_page(self.slug)

    @classmethod
    def get_cache_key_for_page(cls, slug, object_type='view'):
        return 'page-%s-%s' % (slug, object_type)

    @classmethod
    def get_constants(cls):
        return HtmlPage.live.filter(page_type=PageType.CONSTANT_PAGE)

    @classmethod
    def get_child_pages(cls, page_id):
        return HtmlPage.live.filter(parent=page_id).order_by('sort_order')

    @classmethod
    def get_sitemap(cls):
        cache_key = 'pages_sitemap'
        if settings.USE_CACHE:
            sitemap = cache.get(cache_key, None)
            if sitemap:
                return sitemap
        pages = []
        home = HtmlPage.objects.get(slug='home')
        for page in HtmlPage.get_child_pages(home.id):
            pages.append((page, HtmlPage.get_child_pages(page.id)))
        if settings.USE_CACHE:
            cache.set(cache_key, pages, settings.DEFAULT_CACHE_TIMEOUT)
        return pages

    def get_absolute_url(self):
        return reverse('pages_display', args=[self.slug])

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'HTML Page'
        verbose_name_plural = 'HTML Pages'
        ordering = ['sort_order']

    class Admin:
        ordering = ('title')
        prepopulated_fields = {'slug': ('title',)}


def clear_cached_page_view(sender, instance=None, **kwargs):
    if instance is None:
        return
    cache.delete(instance.cache_key)
    cache.delete('sitemap-view')

post_save.connect(clear_cached_page_view, sender=HtmlPage)
