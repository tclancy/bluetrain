from django import forms
from django.conf import settings
from django.contrib import admin
from django.db.models import get_model

from bluetrain.models import *


class CustomFocusAreaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomFocusAreaForm, self).__init__(*args, **kwargs)
        self.fields['link'].queryset = HtmlPage.objects.all().order_by('title')


class FocusAreaAdmin(admin.ModelAdmin):
    form = CustomFocusAreaForm


class PageImageCollectionInline(admin.StackedInline):
    model = PageImageCollection
    extra = 1
    max = 1


class ParentPageField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.parent:
            return '%s - %s' % (obj.parent.title, obj.title)
        return obj.title


class CustomPageForm(forms.ModelForm):
    parent = ParentPageField(queryset=HtmlPage.objects.order_by('parent__title', 'title'), required=False)

    def clean(self):
        if self.instance.id and self.cleaned_data.get('parent', None):
            if self.instance.id == self.cleaned_data['parent'].id:
                raise forms.ValidationError('A page cannot be its own parent')

        # Always return the full collection of cleaned data.
        return super(CustomPageForm, self).clean()

    class Meta:
        model = get_model('bluetrain', 'htmlpage')


class HtmlPageAdmin(admin.ModelAdmin):
    class Media:
        # TODO: only do this if grappelli is present, fix paths
        js = ['%s/js/tiny_mce/tiny_mce.js' % settings.MEDIA_URL,
                  '%s/js/tinymce_setup.js' % settings.MEDIA_URL,]

    form = CustomPageForm

    inlines = [PageImageCollectionInline]
    list_display = ('title', 'parent', 'level_one')
    list_filter = ('page_type', )
    search_fields = ['title']
    exclude = ('slug',)
    ordering = ('title',)

    def queryset(self, request):
        """
        Filter the objects displayed in the change_list to hide some L1s
        """
        qs = super(HtmlPageAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        bad_ids = []
        for page in HtmlPage.get_constants():
            bad_ids.append(page.id)

        return qs.exclude(pk__in=bad_ids)


admin.site.register(get_model('bluetrain', 'htmlpage'), HtmlPageAdmin)
admin.site.register(FocusArea, FocusAreaAdmin)
admin.site.register(PageType)
admin.site.register(PageImage)
