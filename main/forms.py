from django import forms
from django.forms import BooleanField, BaseInlineFormSet
from main.models import Settings


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class SettingsForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Settings
        fields = '__all__'