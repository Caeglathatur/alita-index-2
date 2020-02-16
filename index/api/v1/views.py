"""
Copyright © 2019-2020 Alita Index / Caeglathatur

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

from django.db.models import FilteredRelation, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, views
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.viewsets import GenericViewSet

from ... import models, search
from ...filters import filter_category_tree
from ..permissions import ReadOnly
from . import filters, serializers


class IndexAPIRootView(views.APIView):
    """Lists the URLs of provided list views. Detail views are not listed."""

    class IndexAPIRootViewSchema(AutoSchema):
        def get_operation(self, url, method, *args, **kwargs):
            operation = super().get_operation(url, method, *args, **kwargs)
            operation["responses"]["200"]["content"]["application/json"]["schema"] = {
                "type": "object",
                "properties": {
                    "author-list-url": {"type": "string"},
                    "length-unit-list-url": {"type": "string"},
                    "identifier-type-list-url": {"type": "string"},
                    "category-list-url": {"type": "string"},
                    "tag-list-url": {"type": "string"},
                    "language-list-url": {"type": "string"},
                    "entry-list-url": {"type": "string"},
                    "entry-list-by-category-url": {"type": "string"},
                },
            }
            return operation

    permission_classes = (IsAdminUser | ReadOnly,)
    schema = IndexAPIRootViewSchema()

    def get(self, request):
        return Response(
            {
                "entry-list-url": reverse_lazy("entry-list", request=request),
                "entry-list-by-category-url": reverse_lazy(
                    "entry-list-by-category", request=request
                ),
                "author-list-url": reverse_lazy("author-list", request=request),
                "category-list-url": reverse_lazy("category-list", request=request),
                "tag-list-url": reverse_lazy("tag-list", request=request),
                "identifier-type-list-url": reverse_lazy(
                    "identifier-type-list", request=request
                ),
                "length-unit-list-url": reverse_lazy(
                    "length-unit-list", request=request
                ),
                "language-list-url": reverse_lazy("language-list", request=request),
            }
        )


class EntryViewSet(
    mixins.ListModelMixin,
    # mixins.CreateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    GenericViewSet,
):
    """
    list:
    Lists entries that are in the index.

    retrieve:
    Returns a single entry from the index.
    """

    class EntryViewSetSchema(AutoSchema):
        def get_operation(self, url, method, *args, **kwargs):
            operation = super().get_operation(url, method, *args, **kwargs)
            if self.view.action == "list_by_category":
                operation["parameters"].append(
                    {
                        "name": "tag",
                        "in": "query",
                        "required": False,
                        "description": """Tag `id` to filter by. `null` matches
untagged entries.

Multiple values are supported by repeating the parameter with different values. The
result will be the intersection (AND) of the filters.""",
                        "schema": {"type": "integer"},
                    }
                )
                operation["parameters"].append(
                    {
                        "name": "lang",
                        "in": "query",
                        "required": False,
                        "description": """Lanaguage `code` to filter by. `null`
matches entries with no specified language (language unknown, irrelevant or
unimportant).

Multiple values are supported by repeating the parameter with different values. The
result will be the  union (OR) of the filters.""",
                        "schema": {"type": "string"},
                    }
                )
            return operation

    serializer_class = serializers.EntrySerializer
    permission_classes = (IsAdminUser | ReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = filters.EntryFilterSet
    search_fields = ("title", "description", "url", "keywords")
    schema = EntryViewSetSchema()

    def get_queryset(self):
        qs = models.Entry.objects.filter(is_visible=True)
        return qs

    @action(
        url_path="by-category",
        url_name="list-by-category",
        detail=False,
        methods=["get"],
    )
    def list_by_category(self, request):
        """Lists all entries in the index as they are organized in the category
        tree. The same entry may appear in multiple categories. Empty categories are
        not shown.
        """

        categories = models.Category.objects.filter(parent__isnull=True)
        for cat in categories:
            filter_category_tree(cat, request, [])
        categories = [
            c for c in categories if c.entries_filtered or c.children_filtered
        ]

        s = serializers.CategoryTreeEntrySerializer(categories, many=True)
        return Response(s.data)


class EntrySearchView(views.APIView):
    class EntrySearchViewSchema(AutoSchema):
        def get_operation(self, url, method, *args, **kwargs):
            operation = super().get_operation(url, method, *args, **kwargs)
            operation["parameters"].append(
                {
                    "name": "q",
                    "in": "query",
                    "required": False,
                    "description": (
                        "Search query consisting of space-separated terms."
                    ),
                    "schema": {"type": "string"},
                }
            )
            return operation

    permission_classes = (IsAdminUser | ReadOnly,)
    schema = EntrySearchViewSchema()

    def get(self, request, format=None):
        """Lists entries based on search query. The results are ordered in
        descending order by the number of matching search terms.

        Unlike the <code>search</code> query param of other entry views (which
        is very shallow), this view performs a full text search across relationships
        (entries, sub entries, authors, categories, tags and identifiers).
        """

        query = self.request.GET.get("q", "")
        results = search.search_entries(query)
        results = list(map(lambda e: e[0], results))
        s = serializers.EntrySerializer(results, many=True)
        return Response(s.data)


class CategoryViewSet(
    mixins.ListModelMixin,
    # mixins.CreateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    GenericViewSet,
):
    """
    list:
    Lists categories to which entries can belong as a tree structure.

    retrieve:
    Returns a single category and its children as a tree structure.
    """

    serializer_class = serializers.CategoryTreeSerializer
    permission_classes = (IsAdminUser | ReadOnly,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ("name", "slug")

    def get_queryset(self):
        qs = models.Category.objects.all()
        if self.action == "list":
            qs = qs.filter(parent__isnull=True)
        return qs


class IdentifierTypeViewSet(
    mixins.ListModelMixin,
    # mixins.CreateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    GenericViewSet,
):
    """
    list:
    Lists identifier types.

    retrieve:
    Returns a single identifier type.
    """

    queryset = models.IdentifierType.objects.all()
    serializer_class = serializers.IdentifierTypeSerializer
    permission_classes = (IsAdminUser | ReadOnly,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ("name",)


class LengthUnitViewSet(
    mixins.ListModelMixin,
    # mixins.CreateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    GenericViewSet,
):
    """
    list:
    Lists length units used to describe the lengths of entries.

    retrieve:
    Returns a single length unit used to describe the lengths of entries.
    """

    queryset = models.LengthUnit.objects.all()
    serializer_class = serializers.LengthUnitSerializer
    permission_classes = (IsAdminUser | ReadOnly,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ("name", "name_plural")


class TagViewSet(
    mixins.ListModelMixin,
    # mixins.CreateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    GenericViewSet,
):
    """
    list:
    Lists tags.

    retrieve:
    Returns a single tag.
    """

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAdminUser | ReadOnly,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ("name",)


class AuthorViewSet(
    mixins.ListModelMixin,
    # mixins.CreateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    GenericViewSet,
):
    """
    list:
    Lists authors who have at least one entry in the index.

    retrieve:
    Returns a single author who has at least one entry in the index.
    """

    queryset = (
        models.Author.objects.annotate(
            visible_entries=FilteredRelation(
                "entries", condition=Q(entries__is_visible=True)
            )
        )
        .filter(visible_entries__isnull=False)
        .distinct()
    )
    serializer_class = serializers.AuthorSerializer
    permission_classes = (IsAdminUser | ReadOnly,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ("name", "discriminator", "url")


class LanguageViewSet(
    mixins.ListModelMixin,
    # mixins.CreateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.UpdateModelMixin,
    GenericViewSet,
):
    """
    list:
    Lists languages.

    retrieve:
    Returns a single language.
    """

    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    permission_classes = (IsAdminUser | ReadOnly,)
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ("name", "code")
