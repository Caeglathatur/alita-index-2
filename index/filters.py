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

from django.conf import settings

from django.db.models import Q


def filter_list_intersection(
    queryset, request, param_name, field_name, lookup_expr="exact", type=None
):
    """The value 'null' is reserved for filtering on <field>__isnull=True."""

    values = request.GET.getlist(param_name)

    if "null" in values:
        lookup = "%s__isnull" % (field_name)
        queryset = queryset.filter(**{lookup: True})

    if type == "int":
        values = {int(item) for item in values if item.isdigit()}

    for v in values:
        lookup = "%s__%s" % (field_name, lookup_expr)
        queryset = queryset.filter(**{lookup: v})

    return queryset


def filter_list_union(queryset, request, param_name, field_name, type=None, default=[]):
    """The value 'null' is reserved for filtering on <field>__isnull=True."""

    values = request.GET.getlist(param_name) or default

    values_converted = []
    include_null = "null" in values
    for val in values:
        if val == "null":
            continue
        elif type == "int" and val.isdigit():
            values_converted.append(int(val))
        else:
            values_converted.append(val)
    values = values_converted

    if values or include_null:
        lookup = "%s__in" % field_name
        lookup_null = "%s__isnull" % field_name

        queryset = queryset.filter(
            Q(**{lookup: values}) | Q(**{lookup_null: True})
            if include_null
            else Q(**{lookup: values})
        )

    return queryset


def filter_entries(queryset, request):
    queryset = filter_list_intersection(queryset, request, "tag", "tags", type="int")
    queryset = filter_list_union(
        queryset,
        request,
        "lang",
        "languages",
        default=settings.INDEX_DEFAULT_LANG_FILTER
        if hasattr(settings, "INDEX_DEFAULT_LANG_FILTER")
        else [],
    )
    return queryset


def filter_category_contents(category, request):
    category.entries_filtered = filter_entries(category.entries_visible, request)
    category.entries_filtered_traversed_count = len(category.entries_filtered)
    category.children_filtered = []
    for c in category.children.all():
        filter_category_contents(c, request)
        if c.entries_filtered or c.children_filtered:
            category.children_filtered.append(c)
            category.entries_filtered_traversed_count += (
                c.entries_filtered_traversed_count
            )
