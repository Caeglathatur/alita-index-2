from django.contrib import admin
from . import models


class IdentifierInline(admin.TabularInline):
    model = models.Identifier
    extra = 1


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    inlines = (
        IdentifierInline,
    )


@admin.register(models.Identifier)
class IdentifierAdmin(admin.ModelAdmin):
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


@admin.register(models.MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.IdentifierType)
class IdentifierTypeAdmin(admin.ModelAdmin):
    pass
