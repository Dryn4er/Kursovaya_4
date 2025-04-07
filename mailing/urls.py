from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.services import MailingService
from mailing.views import (MailingCreateView, MailingDeleteView,
                           MailingListView, MailingUpdateView,
                           MessageCreateView, MessageDeleteView,
                           MessageDetailView, MessageListView,
                           MessageUpdateView, RecipientCreateView,
                           RecipientDeleteView, RecipientDetailView,
                           RecipientListView, RecipientUpdateView,
                           StatisticsView, MailingDetailView, homeView,)

app_name = MailingConfig.name

urlpatterns = [
    path("home/", homeView.as_view(), name="home"),
    path("receive_mail/create/", RecipientCreateView.as_view(), name="receive_mail_form"),
    path("receive_mail/list/", RecipientListView.as_view(), name="receive_mail_list"),
    path("receive_mail/<int:pk>/", RecipientDetailView.as_view(), name="receive_mail_detail"),
    path(
        "receive_mail/<int:pk>/update/",
        RecipientUpdateView.as_view(),
        name="receive_mail_update",
    ),
    path(
        "receive_mail/<int:pk>/delete/",
        RecipientDeleteView.as_view(),
        name="receive_mail_delete",
    ),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/list/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path(
        "message/<int:pk>/update/",
        MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "message/<int:pk>/delete/",
        MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("mailing/list/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/statistics/", StatisticsView.as_view(), name="statistics"),
    path(
        "mailing/<int:pk>/stop/",
        MailingUpdateView.stop_mailing,
        name="stop_mailing",
    ),
    path(
        "mailing/update/<int:pk>", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing/<int:pk>/send/", MailingService.send_mailing, name="send_mailing"
    ),
    path(
        "mailing/<int:pk>/delete/",
        MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
]
