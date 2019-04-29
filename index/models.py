from django.db.models import (CASCADE, SET_NULL, BooleanField, CharField,
                              DateTimeField, ForeignKey, ManyToManyField,
                              Model, PositiveIntegerField, TextField,
                              UniqueConstraint, URLField)


class Entry(Model):
    title = CharField(
        max_length=255,
    )
    description = TextField(
        blank=True,
    )
    parent = ForeignKey(
        'self',
        on_delete=SET_NULL,
        related_name='children',
        null=True,
        blank=True,
    )
    url = URLField(
        blank=True,
    )
    media_type = ForeignKey(
        'MediaType',
        related_name='entries',
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    length_seconds = PositiveIntegerField(
        null=True,
        blank=True,
    )
    length_words = PositiveIntegerField(
        null=True,
        blank=True,
    )
    created = DateTimeField(
        auto_now_add=True,
    )
    updated = DateTimeField(
        auto_now=True,
    )
    is_visible = BooleanField(
        default=False,
    )
    categories = ManyToManyField(
        'Category',
        related_name='entries',
    )
    authors = ManyToManyField(
        'Author',
        related_name='entries',
    )
    tags = ManyToManyField(
        'Tag',
        related_name='entries',
    )
    identifiers = ManyToManyField(
        'IdentifierType',
        related_name='entries',
        through='Identifier',
        # through_fields=('entry', 'type'),
    )


class Identifier(Model):
    entry = ForeignKey(
        Entry,
        on_delete=CASCADE,
    )
    type = ForeignKey(
        'IdentifierType',
        on_delete=CASCADE,
    )
    value = CharField(
        max_length=255,
    )


class Category(Model):
    name = CharField(
        max_length=150,
    )
    parent = ForeignKey(
        'self',
        on_delete=SET_NULL,
        related_name='children',
        null=True,
        blank=True,
    )


class Author(Model):

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'discriminator'], name='unique_person')
        ]

    name = CharField(
        max_length=255,
    )
    discriminator = CharField(
        help_text=(
            'Used for distinguishing two people with the same name. '
            'Human-readable and visible to users.'),
        max_length=255,
        blank=True,
    )


class Tag(Model):
    name = CharField(
        max_length=150,
    )


class MediaType(Model):
    name = CharField(
        max_length=150,
    )


class IdentifierType(Model):
    name = CharField(
        max_length=150,
    )
