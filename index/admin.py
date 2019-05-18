"""
Copyright © 2019 Alita Index / Caeglathatur

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

from . import models


class EntryIdentifierInline(admin.TabularInline):
    model = models.EntryIdentifier
    extra = 1


class SubEntryInline(admin.StackedInline):
    model = models.SubEntry
    extra = 1


class SubEntryIdentifierInline(admin.TabularInline):
    model = models.SubEntryIdentifier
    extra = 1


def keyword_count(obj):
    return len(obj.keywords.split())


keyword_count.short_description = "Keywords"


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    inlines = (EntryIdentifierInline, SubEntryInline)
    list_display = ("__str__", "id", "is_visible", keyword_count, "created", "updated")
    list_filter = ("is_visible", "tags", "categories", "authors")
    search_fields = ("title", "description", "keywords")


@admin.register(models.SubEntry)
class SubEntryAdmin(admin.ModelAdmin):
    inlines = (SubEntryIdentifierInline, SubEntryInline)


@admin.register(models.EntryIdentifier)
class EntryIdentifierAdmin(admin.ModelAdmin):
    list_display = ("__str__", "type", "entry")


@admin.register(models.SubEntryIdentifier)
class SubEntryIdentifierAdmin(admin.ModelAdmin):
    list_display = ("__str__", "type", "sub_entry")


@admin.register(models.IdentifierType)
class IdentifierTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "slug", "keywords", "id")


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id", "discriminator", "url")


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "color", "id")


@admin.register(models.LengthUnit)
class LengthUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "code")
