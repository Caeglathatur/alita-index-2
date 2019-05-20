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

from rest_framework import serializers
from ... import models
from rest_framework_recursive.fields import RecursiveField


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ("id", "name", "discriminator", "url")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ("id", "name", "slug", "keywords", "parent", "children")


class CategoryTreeSerializer(serializers.ModelSerializer):
    children = RecursiveField(allow_null=True, many=True)

    class Meta:
        model = models.Category
        fields = ("id", "name", "slug", "keywords", "parent", "children")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ("id", "name", "color", "order")


class IdentifierTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IdentifierType
        fields = ("id", "name")


class EntryIdentifierSerializer(serializers.ModelSerializer):
    type = IdentifierTypeSerializer()

    class Meta:
        model = models.EntryIdentifier
        fields = ("type", "value")


class SubEntryIdentifierSerializer(serializers.ModelSerializer):
    type = IdentifierTypeSerializer()

    class Meta:
        model = models.SubEntryIdentifier
        fields = ("type", "value")


class LengthUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LengthUnit
        fields = ("id", "name", "name_plural")


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = ("code", "name")


class SubEntrySerializer(serializers.ModelSerializer):
    identifiers = EntryIdentifierSerializer(many=True, read_only=True)
    children = RecursiveField(allow_null=True, many=True)
    length_unit = LengthUnitSerializer()
    length_display = serializers.CharField(allow_null=True)

    class Meta:
        model = models.SubEntry
        fields = (
            "title",
            "description",
            "order",
            "url",
            "length",
            "length_unit",
            "length_display",
            "identifiers",
            "children",
        )


class EntrySerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)
    tags = TagSerializer(many=True)
    identifiers = EntryIdentifierSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    children = SubEntrySerializer(allow_null=True, many=True)
    length_unit = LengthUnitSerializer()
    length_display = serializers.CharField(allow_null=True)

    class Meta:
        model = models.Entry
        fields = (
            "id",
            "title",
            "description",
            "keywords",
            "url",
            "length",
            "length_unit",
            "length_display",
            "created",
            "updated",
            "categories",
            "authors",
            "tags",
            "identifiers",
            "languages",
            "children",
        )


class CategoryTreeEntrySerializer(serializers.ModelSerializer):
    entries = EntrySerializer(source="entries_filtered", many=True, allow_null=True)
    children = RecursiveField(source="children_filtered", many=True, allow_null=True)

    class Meta:
        model = models.Category
        fields = ("id", "name", "slug", "keywords", "parent", "entries", "children")
