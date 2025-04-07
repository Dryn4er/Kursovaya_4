import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from config.settings import DEBUG, EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.token = secrets.token_hex(16)
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{user.token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке, чтобы подтвердить почту: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[
                user.email,
            ],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("users:user_detail")

    def get_form_class(self):
        return UserUpdateForm

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    @staticmethod
    def block_user(request, pk):
        block_user = User.objects.get(pk=pk)
        if not request.user.has_per("users.can_block_user"):
            raise PermissionDenied
        else:
            block_user.is_active = False
            block_user.save()
        return redirect(reverse("mailing:home"))


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "mailing/user_list.html"
