from django.db.models import FilteredRelation, Q
from rest_framework import views
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.viewsets import GenericViewSet

from ... import models
from . import filters, serializers
from .permissions import ReadOnly


class IndexAPIRootView(views.APIView):
    """Lists the URLs of provided list views. Detail views are not listed."""

    def get(self, request):
        return Response({
            'entry-list-url': reverse_lazy('entry-list', request=request),
            'entry-list-by-category-url': reverse_lazy(
                'entry-list-by-category',
                request=request,
            ),
            'author-list-url': reverse_lazy(
                'author-list',
                request=request,
            ),
            'category-list-url': reverse_lazy(
                'category-list',
                request=request,
            ),
            'tag-list-url': reverse_lazy(
                'tag-list',
                request=request,
            ),
            'identifier-type-list-url': reverse_lazy(
                'identifier-type-list',
                request=request,
            ),
            'length-unit-list-url': reverse_lazy(
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
    filterset_class = filters.EntryFilterSet

    def get_queryset(self):
        qs = models.Entry.objects.filter(is_visible=True)
        return qs

    @action(
        url_path='by-category',
        url_name='list-by-category',
        detail=False,
        methods=['get'],
    )
    def list_by_category(self, request):
        """Lists all entries as they are organized in the category tree. The
        same entry may appear in multiple categories.
        """

        root_cats = models.Category.objects.filter(
            parent__isnull=True).order_by('name')
        print(root_cats)
        s = serializers.CategoryTreeEntrySerializer(root_cats, many=True)
        return Response(s.data)


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
    queryset = models.Author.objects.annotate(visible_entries=FilteredRelation(
        'entries',
        condition=Q(entries__is_visible=True),
    )).filter(visible_entries__isnull=False).distinct()
    serializer_class = serializers.AuthorSerializer
    permission_classes = (IsAdminUser | ReadOnly,)
