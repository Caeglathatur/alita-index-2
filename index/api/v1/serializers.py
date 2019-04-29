from rest_framework import serializers
from ... import models
from rest_framework_recursive.fields import RecursiveField


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Author
        fields = (
            'id',
            'name',
            'discriminator',
            'url',
        )


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(allow_null=True, many=True)

    class Meta:
        model = models.Category
        fields = (
            'id',
            'name',
            'parent',
            'children',
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = (
            'id',
            'name',
        )


class IdentifierSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='name')

    class Meta:
        model = models.Identifier
        fields = (
            'type',
            'value',
        )


class EntrySerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)
    tags = TagSerializer(many=True)
    identifiers = IdentifierSerializer(many=True, read_only=True)
    children = RecursiveField(allow_null=True, many=True)

    class Meta:
        model = models.Entry
        fields = (
            'id',
            'title',
            'description',
            'url',
            'media_type',
            'length_seconds',
            'length_words',
            'created',
            'updated',
            'categories',
            'authors',
            'tags',
            'identifiers',
            'children',
        )
