from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from ... import models
from . import serializers
from .permissions import ReadOnly


class IndexAPIRootView(views.APIView):
    def get(self, request):
        return Response({
            'entry-list-url': reverse_lazy('entry-list', request=request),
            'author-url': reverse_lazy(
                'author-list',
                request=request,
            ),
            'category-list-url': reverse_lazy(
                'category-list',
                request=request,
            ),
            'tag-url': reverse_lazy(
                'tag-list',
                request=request,
            ),
            'identifier-type-url': reverse_lazy(
                'identifier-type-list',
                request=request,
            ),
            'length-unit-url': reverse_lazy(
                'length-unit-list',
                request=request,
            ),
        })


class EntryViewSet(
    ListModelMixin,
    # CreateModelMixin,
    # DestroyModelMixin,
    RetrieveModelMixin,
    # UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.EntrySerializer
    permission_classes = (IsAdminUser | ReadOnly,)

    def get_queryset(self):
        qs = models.Entry.objects.all()
        return qs


class CategoryViewSet(
    ListModelMixin,
    # CreateModelMixin,
    # DestroyModelMixin,
    RetrieveModelMixin,
    # UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = serializers.CategoryTreeSerializer
    permission_classes = (IsAdminUser | ReadOnly,)

    def get_queryset(self):
        qs = models.Category.objects.all()
        if self.action == 'list':
            qs = qs.filter(parent__isnull=True)
        return qs


class IdentifierTypeViewSet(
    ListModelMixin,
    # CreateModelMixin,
    # DestroyModelMixin,
    RetrieveModelMixin,
    # UpdateModelMixin,
    GenericViewSet,
):
    queryset = models.IdentifierType.objects.all()
    serializer_class = serializers.IdentifierTypeSerializer
    permission_classes = (IsAdminUser | ReadOnly,)


class LengthUnitViewSet(
    ListModelMixin,
    # CreateModelMixin,
    # DestroyModelMixin,
    RetrieveModelMixin,
    # UpdateModelMixin,
    GenericViewSet,
):
    queryset = models.LengthUnit.objects.all()
    serializer_class = serializers.LengthUnitSerializer
    permission_classes = (IsAdminUser | ReadOnly,)


class TagViewSet(
    ListModelMixin,
    # CreateModelMixin,
    # DestroyModelMixin,
    RetrieveModelMixin,
    # UpdateModelMixin,
    GenericViewSet,
):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAdminUser | ReadOnly,)


class AuthorViewSet(
    ListModelMixin,
    # CreateModelMixin,
    # DestroyModelMixin,
    RetrieveModelMixin,
    # UpdateModelMixin,
    GenericViewSet,
):
    queryset = models.Author.objects.filter(entries__isnull=False)
    serializer_class = serializers.AuthorSerializer
    permission_classes = (IsAdminUser | ReadOnly,)
