from django import forms
from .models import Product
from django.core.validators import RegexValidator
from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import FileInput, ClearableFileInput
from django.utils.safestring import mark_safe
from django.utils.html import format_html

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductAdminForm(forms.ModelForm):
    upload_image = MultipleFileField()

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "image",
            "upload_image",
            'category',
            "regular_price",
            "discount",
            "sale_price",
            "status",
        )
