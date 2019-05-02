import markdown
from django.db import models


class BaseEntry:

    @property
    def description_html(self):
        return markdown.markdown(self.description)

    @property
    def length_display(self):
        if not self.length or not self.length_unit:
            return None
        unit = self.length_unit.name \
            if self.length == 1 else self.length_unit.name_plural
        return '{} {}'.format(str(self.length), unit)


class Entry(BaseEntry, models.Model):

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['title']

    title = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        help_text='Supports Markdown.',
        blank=True,
    )
    url = models.URLField(
        verbose_name='URL',
        blank=True,
    )
    # media_type = models.ForeignKey(
    #     'MediaType',
    #     related_name='entries',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )
    length = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    length_unit = models.ForeignKey(
        'LengthUnit',
        related_name='entries',
        on_delete=models.SET_NULL,
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
        through='EntryIdentifier',
        # through_fields=('entry', 'type'),
        blank=True,
    )

    @property
    def identifiers(self):
        return EntryIdentifier.objects.filter(entry=self)

    def __str__(self):
        return self.title


class SubEntry(BaseEntry, models.Model):

    class Meta:
        verbose_name_plural = 'sub entries'
        ordering = ['title']

    title = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        help_text='Supports Markdown.',
        blank=True,
    )
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
    )
    url = models.URLField(
        verbose_name='URL',
        blank=True,
    )
    length = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    length_unit = models.ForeignKey(
        'LengthUnit',
        related_name='sub_entries',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    identifier_types = models.ManyToManyField(
        'IdentifierType',
        related_name='sub_entries',
        through='SubEntryIdentifier',
        # through_fields=('entry', 'type'),
        blank=True,
    )

    @property
    def identifiers(self):
        return SubEntryIdentifier.objects.filter(sub_entry=self)

    def __str__(self):
        path = [self.title]
        next_ancestor = self.parent or self.entry
        while next_ancestor:
            path.append(next_ancestor.title)
            if isinstance(next_ancestor, Entry):
                break
            else:
                next_ancestor = next_ancestor.parent or next_ancestor.entry
        path.reverse()
        return ' / '.join(path)


class EntryIdentifier(models.Model):

    class Meta:
        verbose_name_plural = 'entry identifiers'

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

    def __str__(self):
        return self.value


class SubEntryIdentifier(models.Model):

    class Meta:
        verbose_name_plural = 'sub entry identifiers'

    sub_entry = models.ForeignKey(
        SubEntry,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        'IdentifierType',
        on_delete=models.CASCADE,
    )
    value = models.CharField(
        max_length=255,
    )

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
        ordering = ['name']

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

    @property
    def ancestors(self):
        path = []
        next_ancestor = self.parent
        while next_ancestor:
            path.append(next_ancestor)
            next_ancestor = next_ancestor.parent
        return path

    @property
    def descendants(self):
        descendants = set()
        to_traverse = list(self.children.all())
        while to_traverse:
            descendants |= set(to_traverse)
            next_to_traverse = []
            for d in to_traverse:
                next_to_traverse += d.children.all()
            to_traverse = next_to_traverse
        return descendants

    def __str__(self):
        ancestors = self.ancestors
        ancestors.reverse()
        ancestors.append(self)
        return ' / '.join([a.name for a in ancestors])


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
    )

    def __str__(self):
        return self.name


class LengthUnit(models.Model):
    name = models.CharField(
        help_text='Singular.',
        max_length=150,
    )
    name_plural = models.CharField(
        max_length=150,
    )

    def __str__(self):
        return self.name
