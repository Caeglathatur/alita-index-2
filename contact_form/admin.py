from django.contrib import admin

from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'sent',
        'subject',
        'message',
        'id',
    )
    list_filter = (
        'subject',
    )
    search_fields = (
        'message',
    )


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'id',
    )
    search_fields = (
        'name',
    )
