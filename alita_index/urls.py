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

from django.contrib import admin
from django.urls import include, path

from contact_form.views import ContactFormView, ContactFormSuccessView
from index import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("contact/", ContactFormView.as_view(), name="contact"),
    path("contact/success/", ContactFormSuccessView.as_view(), name="contact-success"),
    path("index-api/", include("index.api.urls")),
    path("newest/", views.NewestView.as_view(), name="newest"),
    path("entries/<int:pk>/", views.EntryDetailView.as_view(), name="entry-detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("rss/", views.RssView.as_view(), name="rss"),
    path("alita-index.md", views.MarkdownView.as_view(), name="markdown"),
    path("captcha/", include("captcha.urls")),
    path("", views.CategoriesView.as_view(), name="categories"),
]
