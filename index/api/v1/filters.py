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
            lookup = '%s__%s' % (self.field_name, self.lookup_expr)
            queryset = queryset.filter(**{lookup: v})

        return queryset


class ListUnionFilter(filters.Filter):

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

        if values:
            lookup = '%s__in' % self.field_name
            queryset = queryset.filter(**{lookup: values})

        return queryset


class CategoryListFilter(filters.Filter):

    def filter(self, queryset, value):
        try:
            request = self.parent.request
        except AttributeError:
            return None

        values = request.GET.getlist('category')
        values = {int(item) for item in values if item.isdigit()}
        categories = models.Category.objects.filter(id__in=values)

        if categories:
            categories_with_descendants = set(categories)
            for c in categories:
                categories_with_descendants |= set(c.descendants)
            queryset = queryset.filter(
                categories__in=[c.id for c in categories_with_descendants])

        return queryset


class EntryFilterSet(filters.FilterSet):
    category = CategoryListFilter(
        help_text='Category <code>id</code> to filter by. Entries in the '
        'child categories of the specified category will be included.'
        '<br><br>Multiple values are supported by repeating the parameter '
        'with different values. The result will be the union (OR) of the '
        'filters.',
    )
    tag = ListIntersectionFilter(
        arg_name='tag',
        field_name='tags',
        help_text='Tag <code>id</code> to filter by.'
        '<br><br>Multiple values are supported by repeating the parameter '
        'with different values. The result will be the intersection (AND) of '
        'the filters.',
    )
    author = ListUnionFilter(
        arg_name='author',
        field_name='authors',
        help_text='Author <code>id</code> to filter by.'
        '<br><br>Multiple values are supported by repeating the parameter '
        'with different values. The result will be the union (OR) of the '
        'filters.',
    )
