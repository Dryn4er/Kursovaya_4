from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import MailAttempt, Mailing, Message, ReceiveMail
from django.utils import timezone
from mailing.services import MailingService


class homeView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Главная"
        context_data["count_mailing"] = len(Mailing.objects.all())
        active_mailings_count = Mailing.objects.filter(status="Создано").count()
        context_data["active_mailings_count"] = active_mailings_count
        unique_clients_count = ReceiveMail.objects.distinct().count()
        context_data["unique_clients_count"] = unique_clients_count
        return context_data


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = ReceiveMail
    template_name = 'mailing/receive_mail_form.html'
    fields = ("email", "name", "comment")
    success_url = reverse_lazy("mailing:receive_mail_list")

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientListView(LoginRequiredMixin, ListView):
    model = ReceiveMail
    template_name = "mailing/receive_mail_list.html"


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = ReceiveMail
    template_name = "mailing/receive_mail_detail.html"

class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = ReceiveMail
    template_name = "mailing/receive_mail_form.html"
    fields = ("email", "name", "comment")

    def get_success_url(self):
        return reverse_lazy("mailing:receive_mail_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return RecipientForm
        raise PermissionDenied


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = ReceiveMail
    template_name = "mailing/receive_mail_delete.html"
    success_url = reverse_lazy("mailing:receive_mail_list")


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ("theme", "content")
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/message_list.html"


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/message_detail.html"


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ("theme", "content")

    def get_success_url(self):
        return reverse_lazy("mailing:message_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return MessageForm
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_delete.html"
    success_url = reverse_lazy("mailing:message_list")


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    # fields = ("start_mailing", "end_mailing", "status", "message", "recipients")
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ("theme", "content")

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return MailingForm
        raise PermissionDenied

    @staticmethod
    def stop_mailing(request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        # Проверка прав доступа (если необходимо)
        if request.user == mailing.owner or request.user.has_perm('mailing.can_stop_mailing'):
            # Устанавливаем время окончания
            mailing.end_mailing = timezone.now()
            mailing.status = 'stopped'  # Обновляем статус, если это необходимо
            mailing.save()

        return redirect('mailing:mailing_list')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user or user.has_perms(["mailing.can_delete_mailing"]):
            return MailingForm
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user

        if self.object.owner == user or user.has_perms(["mailing.can_delete_mailing"]):
            return super().post(request, *args, **kwargs)

        raise PermissionDenied


class StatisticsView(TemplateView):
    template_name = "mailing/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        mailings = Mailing.objects.filter(owner=user)
        attempts = MailAttempt.objects.filter(mailing__in=mailings)
        successful = attempts.filter(status="success").count()
        failed = attempts.filter(status="failure").count()
        mailing_count = sum(attempt.mailing.recipients.count() for attempt in attempts if attempt.status == "success")

        context["successful"] = successful
        context["failed"] = failed
        context["mailing_count"] = mailing_count
        context["attempts"] = attempts.count()

        return context


