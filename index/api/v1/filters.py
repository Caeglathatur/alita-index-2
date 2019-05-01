from django_filters import rest_framework as filters

from ... import models


class ListOrFilter(filters.Filter):

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


class ListAndFilter(filters.Filter):

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
    category = CategoryListFilter()
    tag = ListOrFilter(arg_name='tag', field_name='tags')
    author = ListAndFilter(arg_name='author', field_name='authors')
