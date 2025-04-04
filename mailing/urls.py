from django.urls import include, path
from django.views.decorators.cache import cache_page
from . import views
from django.conf import settings
from django.conf.urls.static import static

from mailing.apps import MailingConfig
from mailing.services import block_mailing, run_mail
from mailing.views import (Contacts, MailingAttemptCreateView, MailingAttemptListView, MailingCreateView,
                           MailingDeleteView, MailingDetailView,
                           MailingListView, MailingUpdateView, MessageCreateView, MessageDeleteView,
                           MessageDetailView, MessageListView,
                           MessageUpdateView, ReceiveMailCreateView, ReceiveMailDetailView, ReceiveMailingDeleteView,
                           ReceiveMailListView,
                           ReceiveMailUpdateView, homeView, Messages)

app_name = MailingConfig.name

urlpatterns = [
    path("home/", homeView.as_view(), name="home"),
    path("contacts/", cache_page(60)(Contacts.as_view()), name="contacts"),
    path("message/", Messages.as_view(), name="message"),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>/run_mail/", run_mail, name="run_mail"),
    path("mailing/<int:pk>/detail/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/new/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/edit/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("receive_mail/", ReceiveMailListView.as_view(), name="receive_mail_list"),
    path("receive_mail/<int:pk>/detail/", cache_page(60)(ReceiveMailDetailView.as_view()), name="receive_mail_detail"),
    path("receive_mail/create/", ReceiveMailCreateView.as_view(), name="receive_mail_form"),
    path("receive_mail/<int:pk>/delete/", ReceiveMailingDeleteView.as_view(), name="receive_mail_delete"),
    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/detail/", MessageDetailView.as_view(), name="message_detail"),
    path("message/new/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("send/", MailingAttemptListView.as_view(), name="send_list"),
    path("send/create/", MailingAttemptCreateView.as_view(), name="send_create"),
    path("attempt/", MailingAttemptListView.as_view(), name="attempt"),
    path("block_mailing/<int:pk>", block_mailing, name="block_mailing"),
]