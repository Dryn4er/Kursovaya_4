from django.utils import timezone

from django import forms
from django.forms import BooleanField, ModelForm

from mailing.models import Mailing, Message, ReceiveMail


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = ("theme", "content")


class RecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = ReceiveMail
        fields = ("email", "name", "comment")


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = ("message", "recipients")  # Указываем только нужные поля

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Сохраняем пользователя для дальнейшего использования
        super(MailingForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields["message"].queryset = Message.objects.filter(owner=self.user)
            self.fields["recipients"].queryset = ReceiveMail.objects.filter(owner=self.user)

        self.fields["start_mailing"] = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
        self.fields["end_mailing"] = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
        self.fields["status"] = forms.ChoiceField(
            choices=[('created', 'Создана')],
            initial='created',
            widget=forms.HiddenInput()
        )

    def save(self, commit=True):
        mailing_instance = super(MailingForm, self).save(commit=False)
        mailing_instance.status = 'created'
        mailing_instance.start_mailing = timezone.now()
        mailing_instance.end_mailing = timezone.now()

        if commit:
            mailing_instance.save()

        return mailing_instance

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        return form