from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm
from django.forms import ModelForm
from django.urls import reverse_lazy
from django import forms
from mailing.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Убедитесь, что 'username' включен
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Это имя пользователя уже занято.")
        return username

    def form_valid(self, form):
        print(form.cleaned_data)  # Выводим очищенные данные формы для отладки
        user = form.save()


class UserUpdateForm(StyleFormMixin, ModelForm):

    class Meta:
        model = User
        fields = "__all__"
        exclude = ("token",)

        success_url = reverse_lazy("users:users")


class UserForgotPasswordForm(PasswordResetForm):
    """Форма запроса на восстановление пароля"""

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserSetNewPasswordForm(SetPasswordForm):
    """Форма изменения пароля пользователя после подтверждения"""

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class PasswordRecoveryForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(label="Укажите Email")

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такого email нет в системе")
        return email