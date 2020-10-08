"""
Copyright © 2019-2020 Alita Index / Caeglathatur

This file is part of Alita Index.

Alita Index is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License version 3 as
published by the Free Software Foundation.

Alita Index is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Alita Index.  If not, see <https://www.gnu.org/licenses/>.
"""

from django.contrib import admin
from django.utils.html import format_html

from . import models


class ChoiceInline(admin.StackedInline):
    model = models.Choice


class PollAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]
    list_display = [
        "id",
        "link",
        "question",
        "is_public",
        "is_anonymous",
        "is_open",
        "end_datetime",
        "created",
        "modified",
    ]

    def link(self, obj):
        return format_html(
            '<a href="{}">{}</a>', obj.get_absolute_url(), obj.get_absolute_url()
        )

    link.short_description = "Link"


admin.site.register(models.Poll, PollAdmin)


class VoterAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "is_public",
        "is_active",
        "created",
        "modified",
    ]


admin.site.register(models.Voter, VoterAdmin)


class PollFilter(admin.SimpleListFilter):
    title = "poll"
    parameter_name = "poll"

    def lookups(self, request, model_admin):
        print(models.Poll.objects.all().values("id", "question"))
        return [
            (p["id"], p["question"])
            for p in models.Poll.objects.all().values("id", "question")
        ]

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(poll=self.value())
        return queryset


class VoteAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "link",
        "poll",
        "voter",
        "choice",
        "created",
        "modified",
    ]
    list_filter = [PollFilter, "voter"]

    def link(self, obj):
        return format_html(
            '<a href="{}">{}</a>', obj.get_absolute_url(), obj.get_absolute_url()
        )

    link.short_description = "Link"


admin.site.register(models.Vote, VoteAdmin)
