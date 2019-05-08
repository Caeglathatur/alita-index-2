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
    list_display = (
        '__str__',
        'id',
        'is_visible',
        'created',
    )
    list_filter = (
        'is_visible',
        'tags',
        'categories',
        'authors',
    )
    search_fields = (
        'title',
        'description',
    )


@admin.register(models.SubEntry)
class SubEntryAdmin(admin.ModelAdmin):
    inlines = (
        SubEntryIdentifierInline,
        SubEntryInline,
    )


@admin.register(models.EntryIdentifier)
class EntryIdentifierAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'type',
        'entry',
    )


@admin.register(models.SubEntryIdentifier)
class SubEntryIdentifierAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'type',
        'sub_entry',
    )


@admin.register(models.IdentifierType)
class IdentifierTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'id',
        'discriminator',
        'url',
    )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'id',
        'color',
    )


@admin.register(models.LengthUnit)
class LengthUnitAdmin(admin.ModelAdmin):
    pass
