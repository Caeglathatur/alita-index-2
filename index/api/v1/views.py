from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from ...models import Entry
from .permissions import ReadOnly
from .serializers import EntrySerializer


class EntryViewSet(
    ListModelMixin,
    # CreateModelMixin,
    # DestroyModelMixin,
    RetrieveModelMixin,
    # UpdateModelMixin,
    GenericViewSet,
):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = (IsAdminUser | ReadOnly,)
