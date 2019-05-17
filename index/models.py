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

import markdown
from django.db import models

from . import utils


class BaseEntry:
    @property
    def description_html(self):
        return markdown.markdown(self.description)

    @property
    def description_oneline(self):
        return utils.remove_newlines(
            self.description if self.description else ""
        ).strip()

    @property
    def length_display(self):
        if not self.length or not self.length_unit:
            return None
        # We make no assmuptions about what IDs these units have in the DB.
        # Therefore we identify them by name.
        if self.length_unit.name == "second":
            return utils.format_seconds(self.length)
        if self.length_unit.name == "minute":
            return utils.format_minutes(self.length)
        if self.length_unit.name == "word":
            return utils.format_word_count(self.length)
        return "{} {}".format(
            str(self.length),
            self.length_unit.name if self.length == 1 else self.length_unit.name_plural,
        )


class Entry(BaseEntry, models.Model):
    class Meta:
        verbose_name_plural = "entries"
        ordering = ["title"]

    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Supports Markdown.", blank=True)
    keywords = models.TextField(
        help_text=(
            "Space-separated keywords to improve text search. Normally not directly "
            "visible in the UI, but is returned in the API. Adding keywords that occur "
            "anywhere else (e.g. title, desc., URL, tags, categ., authors, sub "
            "entries) is redundant."
        ),
        blank=True,
    )
    url = models.URLField(verbose_name="URL", blank=True)
    length = models.PositiveIntegerField(null=True, blank=True)
    length_unit = models.ForeignKey(
        "LengthUnit",
        related_name="entries",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=False)
    categories = models.ManyToManyField("Category", related_name="entries", blank=True)
    authors = models.ManyToManyField("Author", related_name="entries", blank=True)
    tags = models.ManyToManyField("Tag", related_name="entries", blank=True)
    identifier_types = models.ManyToManyField(
        "IdentifierType",
        related_name="entries",
        through="EntryIdentifier",
        # through_fields=('entry', 'type'),
        blank=True,
    )

    @property
    def identifiers(self):
        return EntryIdentifier.objects.filter(entry=self)

    @property
    def categories_names(self):
        return list(map(lambda c: c.path_str, self.categories.all()))

    @property
    def authors_names(self):
        return list(map(lambda c: c.name, self.authors.all()))

    @property
    def created_rss(self):
        return self.created.strftime("%a, %d %b %Y %H:%M:%S %z")

    def __str__(self):
        return self.title


class SubEntry(BaseEntry, models.Model):
    class Meta:
        verbose_name_plural = "sub entries"
        ordering = ["order", "title"]

    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Supports Markdown.", blank=True)
    order = models.IntegerField(null=True, blank=True)
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )
    url = models.URLField(verbose_name="URL", blank=True)
    length = models.PositiveIntegerField(null=True, blank=True)
    length_unit = models.ForeignKey(
        "LengthUnit",
        related_name="sub_entries",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    identifier_types = models.ManyToManyField(
        "IdentifierType",
        related_name="sub_entries",
        through="SubEntryIdentifier",
        # through_fields=('entry', 'type'),
        blank=True,
    )

    @property
    def identifiers(self):
        return SubEntryIdentifier.objects.filter(sub_entry=self)

    @property
    def entry_traversed(self):
        if self.entry:
            return self.entry
        next_ancestor = self.parent
        while next_ancestor:
            if isinstance(next_ancestor, Entry):
                break
            else:
                next_ancestor = next_ancestor.parent or next_ancestor.entry
        return next_ancestor

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
        return " / ".join(path)


class EntryIdentifier(models.Model):
    class Meta:
        verbose_name_plural = "entry identifiers"

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    type = models.ForeignKey("IdentifierType", on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class SubEntryIdentifier(models.Model):
    class Meta:
        verbose_name_plural = "sub entry identifiers"

    sub_entry = models.ForeignKey(SubEntry, on_delete=models.CASCADE)
    type = models.ForeignKey("IdentifierType", on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    @property
    def entry(self):
        return self.sub_entry.entry_traversed

    def __str__(self):
        return self.value


class IdentifierType(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    name = models.CharField(max_length=150)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
    )
    slug = models.SlugField(unique=True)
    keywords = models.TextField(
        help_text=(
            "Space-separated keywords to improve text search. Normally not directly "
            "visible in the UI, but is returned in the API. Adding keywords that occur "
            "in the title or parents is redundant."
        ),
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

    @property
    def entries_visible(self):
        return self.entries.filter(is_visible=True)

    @property
    def entries_visible_traversed(self):
        entries = set(self.entries_visible)
        for child in self.children.all():
            entries |= set(child.entries_visible_traversed)
        return list(entries)

    @property
    def path_str(self):
        ancestors = self.ancestors
        ancestors.reverse()
        ancestors.append(self)
        return " / ".join([a.name for a in ancestors])

    def __str__(self):
        return self.path_str


class Author(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "discriminator"], name="unique_person"
            )
        ]

    name = models.CharField(max_length=255)
    discriminator = models.CharField(
        help_text=(
            "Used for distinguishing two people with the same name. "
            "Human-readable and visible to users."
        ),
        max_length=255,
        blank=True,
    )
    url = models.URLField(blank=True)

    @property
    def entries_visible(self):
        return self.entries.filter(is_visible=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=150)
    color = models.CharField(
        help_text="CSS color.", max_length=50, null=True, blank=True, default=None
    )

    @property
    def entries_visible(self):
        return self.entries.filter(is_visible=True)

    def __str__(self):
        return self.name


class LengthUnit(models.Model):
    name = models.CharField(help_text="Singular.", max_length=150)
    name_plural = models.CharField(max_length=150)

    def __str__(self):
        return self.name
