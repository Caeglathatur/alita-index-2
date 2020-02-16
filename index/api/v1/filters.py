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

from django_filters import rest_framework as filters

from ... import models


class ListIntersectionFilter(filters.Filter):
    def __init__(self, arg_name, *args, **kwargs):
        self.arg_name = arg_name
        return super().__init__(*args, **kwargs)

    def filter(self, queryset, value):
        try:
            request = self.parent.request
        except AttributeError:
            return None

        values = request.GET.getlist(self.arg_name)
        values = {int(item) for item in values if item.isdigit()}

        for v in values:
            lookup = "%s__%s" % (self.field_name, self.lookup_expr)
            queryset = queryset.filter(**{lookup: v})

        return queryset


class ListUnionFilter(filters.Filter):
    def __init__(self, arg_name, type=None, *args, **kwargs):
        self.arg_name = arg_name
        self.type = type
        return super().__init__(*args, **kwargs)

    def filter(self, queryset, value):
        try:
            request = self.parent.request
        except AttributeError:
            return None

        values = request.GET.getlist(self.arg_name)
        if self.type == "int":
            values = {int(item) for item in values if item.isdigit()}

        if values:
            lookup = "%s__in" % self.field_name
            queryset = queryset.filter(**{lookup: values})

        return queryset


class CategoryListFilter(filters.Filter):
    def filter(self, queryset, value):
        try:
            request = self.parent.request
        except AttributeError:
            return None

        values = request.GET.getlist("category")
        values = {int(item) for item in values if item.isdigit()}
        categories = models.Category.objects.filter(id__in=values)

        if categories:
            categories_with_descendants = set(categories)
            for c in categories:
                categories_with_descendants |= set(c.descendants)
            queryset = queryset.filter(
                categories__in=[c.id for c in categories_with_descendants]
            )

        return queryset


class EntryFilterSet(filters.FilterSet):
    category = CategoryListFilter(
        label="""Filter by category `id`. Entries in the child categories of the
specified category will be included.

Multiple values are supported by repeating the parameter with different values. The
result will be the union (OR) of the filters.""",
    )
    tag = ListIntersectionFilter(
        arg_name="tag",
        field_name="tags",
        label="""Filter by tag `id`.

Multiple values are supported by repeating the parameter with different values. The
result will be the intersection (AND) of the filters.""",
    )
    author = ListUnionFilter(
        arg_name="author",
        type="int",
        field_name="authors",
        label="""Filter by author `id`.

Multiple values are supported by repeating the parameter with different values. The
result will be the union (OR) of the filters.""",
    )
    lang = ListUnionFilter(
        arg_name="lang",
        field_name="languages",
        label="""Filter by language `code`.

Multiple values are supported by repeating the parameter with different values. The
result will be the union (OR) of the filters.""",
    )
