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

    class Meta:
        model = models.Category
        fields = (
            'id',
            'name',
            'parent',
            'children',
        )


class CategoryTreeSerializer(serializers.ModelSerializer):
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


class IdentifierTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IdentifierType
        fields = (
            'id',
            'name',
        )


class EntryIdentifierSerializer(serializers.ModelSerializer):
    type = IdentifierTypeSerializer()

    class Meta:
        model = models.EntryIdentifier
        fields = (
            'type',
            'value',
        )


class SubEntryIdentifierSerializer(serializers.ModelSerializer):
    type = IdentifierTypeSerializer()

    class Meta:
        model = models.SubEntryIdentifier
        fields = (
            'type',
            'value',
        )


class LengthUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LengthUnit
        fields = (
            'id',
            'name',
            'name_plural',
        )


class SubEntrySerializer(serializers.ModelSerializer):
    identifiers = EntryIdentifierSerializer(many=True, read_only=True)
    children = RecursiveField(allow_null=True, many=True)
    length_unit = LengthUnitSerializer()

    class Meta:
        model = models.Entry
        fields = (
            'title',
            'description',
            'url',
            'length',
            'length_unit',
            'identifiers',
            'children',
        )


class EntrySerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)
    tags = TagSerializer(many=True)
    identifiers = EntryIdentifierSerializer(many=True, read_only=True)
    children = SubEntrySerializer(allow_null=True, many=True)
    length_unit = LengthUnitSerializer()
    # media_type = serializers.CharField(
    #     source='media_type.name',
    #     allow_null=True,
    # )

    class Meta:
        model = models.Entry
        fields = (
            'id',
            'title',
            'description',
            'url',
            # 'media_type',
            'length',
            'length_unit',
            'created',
            'updated',
            'categories',
            'authors',
            'tags',
            'identifiers',
            'children',
        )
