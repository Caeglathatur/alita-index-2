from django.db import models


class Entry(models.Model):

    class Meta:
        verbose_name_plural = 'entries'

    title = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        blank=True,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='children',
        null=True,
        blank=True,
    )
    url = models.URLField(
        verbose_name='URL',
        blank=True,
    )
    media_type = models.ForeignKey(
        'MediaType',
        related_name='entries',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    length_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    length_words = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    is_visible = models.BooleanField(
        default=False,
    )
    categories = models.ManyToManyField(
        'Category',
        related_name='entries',
        blank=True,
    )
    authors = models.ManyToManyField(
        'Author',
        related_name='entries',
        blank=True,
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='entries',
        blank=True,
    )
    identifier_types = models.ManyToManyField(
        'IdentifierType',
        related_name='entries',
        through='Identifier',
        # through_fields=('entry', 'type'),
        blank=True,
    )

    @property
    def identifiers(self):
        return Identifier.objects.filter(entry=self)

    def __str__(self):
        return self.title


class Identifier(models.Model):

    class Meta:
        verbose_name_plural = 'identifiers'

    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        'IdentifierType',
        on_delete=models.CASCADE,
    )
    value = models.CharField(
        max_length=255,
    )

    @property
    def name(self):
        return self.type.name

    def __str__(self):
        return self.value


class IdentifierType(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
    )

    def __str__(self):
        return self.name


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'categories'

    name = models.CharField(
        max_length=150,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='children',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Author(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'discriminator'], name='unique_person')
        ]

    name = models.CharField(
        max_length=255,
    )
    discriminator = models.CharField(
        help_text=(
            'Used for distinguishing two people with the same name. '
            'Human-readable and visible to users.'),
        max_length=255,
        blank=True,
    )
    url = models.URLField(
        blank=True,
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
    )

    def __str__(self):
        return self.name


class MediaType(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
    )

    def __str__(self):
        return self.name
