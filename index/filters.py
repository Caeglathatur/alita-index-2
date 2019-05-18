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

# from . import models


def filter_list_intersection(
    queryset, request, param_name, field_name, lookup_expr="exact", type=None
):
    values = request.GET.getlist(param_name)

    if type == "int":
        if "null" in values:
            lookup = "%s__isnull" % (field_name)
            queryset = queryset.filter(**{lookup: True})
        values = {int(item) for item in values if item.isdigit()}

    for v in values:
        lookup = "%s__%s" % (field_name, lookup_expr)
        queryset = queryset.filter(**{lookup: v})

    return queryset


# def filter_list_union(
#     queryset, request, param_name, field_name, lookup_expr="exact", type=None
# ):
#     values = request.GET.getlist(param_name)
#     if type == "int":
#         values = {int(item) for item in values if item.isdigit()}

#     if values:
#         lookup = "%s__%s" % field_name, lookup_expr
#         queryset = queryset.filter(**{lookup: values})

#     return queryset


def filter_entries(queryset, request):
    queryset = filter_list_intersection(queryset, request, "tag", "tags", type="int")
    return queryset


def filter_category_contents(category, request):
    category.entries_filtered = filter_entries(category.entries_visible, request)
    category.children_filtered = []
    for c in category.children.all():
        filter_category_contents(c, request)
        if c.entries_filtered or c.children_filtered:
            category.children_filtered.append(c)
