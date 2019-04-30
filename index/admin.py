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


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    inlines = (
        EntryIdentifierInline,
        SubEntryInline,
    )


@admin.register(models.SubEntry)
class SubEntryAdmin(admin.ModelAdmin):
    inlines = (
        SubEntryIdentifierInline,
        SubEntryInline,
    )


@admin.register(models.EntryIdentifier)
class EntryIdentifierAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SubEntryIdentifier)
class SubEntryIdentifierAdmin(admin.ModelAdmin):
    pass


@admin.register(models.IdentifierType)
class IdentifierTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.MediaType)
# class MediaTypeAdmin(admin.ModelAdmin):
#     pass


@admin.register(models.LengthUnit)
class LengthUnitAdmin(admin.ModelAdmin):
    pass
