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
        fields = ("start_mailing", "end_mailing", "status", "message", "recipients")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["end_mailing"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        )
        self.fields["start_mailing"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        )

        if user:
            self.fields["message"].queryset = Message.objects.filter(owner=user)
            self.fields["recipients"].queryset = ReceiveMail.objects.filter(owner=user)