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
            'category-list-url': reverse_lazy(
                'category-list',
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
        # if self.action == 'list':
        #     qs = qs.filter(parent__isnull=True)
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
