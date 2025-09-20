# apps/tourism/widgets.py
from django.forms.widgets import Select

class LinkedSelect(Select):
    def __init__(self, attrs=None, choices=(), parent_field=None, ajax_url=None):
        self.parent_field = parent_field
        self.ajax_url = ajax_url
        super().__init__(attrs, choices)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-parent-field'] = self.parent_field
        attrs['data-ajax-url'] = self.ajax_url
        return attrs

    class Media:
        js = ('js/linked_select.js',)
