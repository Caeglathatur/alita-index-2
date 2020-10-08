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

from functools import reduce

from django.conf import settings
from django.views import generic

from . import filters, models, search

DEFAULT_LANG_FILTER = (
    settings.INDEX_DEFAULT_LANG_FILTER
    if hasattr(settings, "INDEX_DEFAULT_LANG_FILTER")
    else []
)


class CategoriesView(generic.TemplateView):
    id = "categories"
    template_name = "index/categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = models.Category.objects.filter(parent__isnull=True)
        for cat in categories:
            filters.filter_category_tree(cat, self.request, DEFAULT_LANG_FILTER)
        categories = [
            c for c in categories if c.entries_filtered or c.children_filtered
        ]
        context["categories"] = categories
        context["entries_count"] = len(
            reduce(
                lambda all, additional: all | additional,
                [c.entries_filtered_traversed_unique for c in categories],
                set(),
            )
        )

        context["tags"] = models.Tag.objects.all()
        context["tags_selected"] = [
            int(t) for t in self.request.GET.getlist("tag") if t.isdigit()
        ]
        if "null" in self.request.GET.getlist("tag"):
            context["tags_selected"].append("null")

        context["langs"] = models.Language.objects.all()
        context["langs_selected"] = self.request.GET.getlist("lang") or (
            DEFAULT_LANG_FILTER
        )

        context["filters_are_active"] = bool(self.request.GET)

        return context


class NewestView(generic.ListView):
    id = "newest"
    queryset = models.Entry.objects.filter(is_visible=True).order_by("-created")
    template_name = "index/newest.html"
    context_object_name = "entries"


class EntryDetailView(generic.DetailView):
    id = "entry-detail"
    queryset = models.Entry.objects.filter(is_visible=True)
    template_name = "index/entry-detail.html"
    context_object_name = "entry"


class SearchView(generic.TemplateView):
    id = "search"
    template_name = "index/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q", "")
        results = search.search_entries(query)

        context["query"] = query
        context["entries"] = results
        return context


class RssView(generic.TemplateView):
    template_name = "index/rss.xml"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["entries"] = models.Entry.objects.filter(is_visible=True).order_by(
            "created"
        )
        return context

    def get(self, *args, **kwargs):
        return self.render_to_response(
            self.get_context_data(), content_type="application/rss+xml; charset=utf-8"
        )


class MarkdownView(generic.TemplateView):
    template_name = "index/markdown.md"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = models.Category.objects.filter(parent__isnull=True)
        for cat in categories:
            filters.filter_category_tree(cat, self.request, DEFAULT_LANG_FILTER)
        categories = [
            c for c in categories if c.entries_filtered or c.children_filtered
        ]
        context["categories"] = categories

        return context

    def get(self, *args, **kwargs):
        return self.render_to_response(
            self.get_context_data(), content_type="text/plain; charset=utf-8"
        )
