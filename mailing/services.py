import smtplib

from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from config.settings import CACHE_ENABLED, EMAIL_HOST_USER
from mailing.models import MailAttempt, Mailing


class MailingService:

    @staticmethod
    def send_mailing(request, pk):
        mailing = Mailing.objects.get(pk=pk)
        subject = mailing.message.theme
        message = mailing.message.content
        recipients = [recipient.email for recipient in mailing.recipients.all()]

        start_mailing = timezone.now()

        try:
            response = send_mail(
                subject, message, EMAIL_HOST_USER, recipients, fail_silently=False
            )
        except smtplib.SMTPException as e:
            MailingService.make_attempt(
                status="failure", response=e, mailing=mailing
            )
        else:
            end_mailing = timezone.now()
            MailingService.make_attempt(
                status="success", response=response, mailing=mailing
            )
            MailingService.update_status(
                mailing=mailing,
                start_mailing=start_mailing,
                end_mailing=end_mailing,
            )
        finally:
            return redirect(reverse("mailing:mailing_list"))

    @staticmethod
    def make_attempt(status, response, mailing):
        attempt = MailAttempt.objects.create(
            status=status, response=response, mailing=mailing
        )
        attempt.save()

    @staticmethod
    def update_status(mailing, start_mailing, end_mailing):
        mailing.start_mailing = timezone.localtime(start_mailing)
        mailing.end_mailing = timezone.localtime(end_mailing)
        mailing.status = "completed"
        mailing.save()

    @staticmethod
    def caching(queryset, model, user=None):
        if not CACHE_ENABLED:
            return queryset.filter(owner=user)
        key = str(model) + "_list"
        objects = cache.get(key)
        if objects is not None:
            return objects
        objects = queryset.filter(owner=user)
        cache.set(key, objects, 60 * 1)
        return objects