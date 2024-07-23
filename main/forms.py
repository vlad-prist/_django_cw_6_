from django import forms
from django.forms import BooleanField, BaseInlineFormSet
from main.models import Settings, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class SettingsForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['clients'].queryset = Client.objects.filter(owner=user)
        # self.fields['message'].queryset = Message.objects.filter(owner=user)

    class Meta:
        model = Settings
        exclude = ('owner',)


class SettingsManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('message', 'clients',)


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('is_banned', 'owner',)


class ClientManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Message
        exclude = ('owner',)


class MessageManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
