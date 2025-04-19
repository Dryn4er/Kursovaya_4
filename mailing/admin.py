from django.contrib import admin

from mailing.models import Mailing, Message, ReceiveMail


@admin.register(ReceiveMail)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "comment")
    search_fields = ("name",)
    ordering = ("email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("theme", "content")
    search_fields = ("theme",)
    ordering = ("theme",)


@admin.register(Mailing)
class MailshotAdmin(admin.ModelAdmin):
    list_display = ("message",)
    list_filter = ("status",)
    search_field = ("message",)