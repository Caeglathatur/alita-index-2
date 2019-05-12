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

from django.views.generic import ListView, TemplateView

from . import models, search


class CategoriesView(TemplateView):
    id = "categories"
    template_name = "index/categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = models.Category.objects.filter(parent__isnull=True)
        return context


class NewestView(ListView):
    id = "newest"
    queryset = models.Entry.objects.filter(is_visible=True).order_by("-created")
    template_name = "index/newest.html"
    context_object_name = "entries"


class SearchView(TemplateView):
    id = "search"
    template_name = "index/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q", "")
        results = search.search_entries(query)

        context["query"] = query
        context["entries"] = results
        return context


class RssView(TemplateView):
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


class MarkdownView(TemplateView):
    template_name = "index/markdown.md"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = models.Category.objects.filter(parent__isnull=True)
        return context

    def get(self, *args, **kwargs):
        return self.render_to_response(
            self.get_context_data(), content_type="text/plain; charset=utf-8"
        )
