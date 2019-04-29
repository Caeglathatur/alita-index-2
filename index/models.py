from django.db.models import (CASCADE, SET_NULL, BooleanField, CharField,
                              DateTimeField, ForeignKey, ManyToManyField,
                              Model, PositiveIntegerField, TextField,
                              UniqueConstraint, URLField)


class Entry(Model):

    class Meta:
        verbose_name_plural = 'entries'

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
        verbose_name='URL',
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
        blank=True,
    )
    authors = ManyToManyField(
        'Author',
        related_name='entries',
        blank=True,
    )
    tags = ManyToManyField(
        'Tag',
        related_name='entries',
        blank=True,
    )
    identifiers = ManyToManyField(
        'IdentifierType',
        related_name='entries',
        through='Identifier',
        # through_fields=('entry', 'type'),
        blank=True,
    )

    def __str__(self):
        return self.title


class Identifier(Model):

    class Meta:
        verbose_name_plural = 'identifiers'

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

    def __str__(self):
        return self.value


class Category(Model):

    class Meta:
        verbose_name_plural = 'categories'

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

    def __str__(self):
        return self.name


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
    url = URLField(
        blank=True,
    )

    def __str__(self):
        return self.name


class Tag(Model):
    name = CharField(
        max_length=150,
    )

    def __str__(self):
        return self.name


class MediaType(Model):
    name = CharField(
        max_length=150,
    )

    def __str__(self):
        return self.name


class IdentifierType(Model):
    name = CharField(
        max_length=150,
    )

    def __str__(self):
        return self.name
