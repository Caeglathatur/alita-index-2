from rest_framework.serializers import ModelSerializer
from ...models import Entry


class EntrySerializer(ModelSerializer):

    class Meta:
        model = Entry
        fields = (
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
        )
