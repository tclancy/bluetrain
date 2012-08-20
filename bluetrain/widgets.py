from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe


class WYMEditor(forms.Textarea):
    class Media:
        js = (
            'js/jquery.js',
            'js/wymeditor/jquery.wymeditor.pack.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'wymeditor'}
        if attrs:
            self.attrs.update(attrs)
        super(WYMEditor, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(WYMEditor, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            jQuery('#id_%s').wymeditor({
                updateSelector: '.submit-row input[type=submit]',
                updateEvent: 'click',
                lang: '%s',
                toolsItems: [
                    {'name': 'Bold', 'title': 'Strong', 'css': 'wym_tools_strong'},
                    {'name': 'Italic', 'title': 'Emphasis', 'css': 'wym_tools_emphasis'},
                    {'name': 'Superscript', 'title': 'Superscript', 'css': 'wym_tools_superscript'},
                    {'name': 'Subscript', 'title': 'Subscript', 'css': 'wym_tools_subscript'},
                    {'name': 'InsertOrderedList', 'title': 'Ordered_List', 'css': 'wym_tools_ordered_list'},
                    {'name': 'InsertUnorderedList', 'title': 'Unordered_List', 'css': 'wym_tools_unordered_list'},
                    {'name': 'Indent', 'title': 'Indent', 'css': 'wym_tools_indent'},
                    {'name': 'Outdent', 'title': 'Outdent', 'css': 'wym_tools_outdent'},
                    {'name': 'Undo', 'title': 'Undo', 'css': 'wym_tools_undo'},
                    {'name': 'Redo', 'title': 'Redo', 'css': 'wym_tools_redo'},
                    {'name': 'CreateLink', 'title': 'Link', 'css': 'wym_tools_link'},
                    {'name': 'Unlink', 'title': 'Unlink', 'css': 'wym_tools_unlink'},
                    {'name': 'Paste', 'title': 'Paste_From_Word', 'css': 'wym_tools_paste'},
                    {'name': 'ToggleHtml', 'title': 'HTML', 'css': 'wym_tools_html'},
                    {'name': 'Preview', 'title': 'Preview', 'css': 'wym_tools_preview'}
                ],
                containersHtml: '',
                classesHtml: ''
            });
            </script>''' % (name, self.language))
