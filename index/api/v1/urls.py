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

from django.urls import path
from rest_framework import routers

from . import views


app_name = "index-api-v1"

router = routers.SimpleRouter()
router.register(r"entries", views.EntryViewSet, basename="entry")
router.register(r"categories", views.CategoryViewSet, basename="category")
router.register(r"length-units", views.LengthUnitViewSet, basename="length-unit")
router.register(
    r"identifier-types", views.IdentifierTypeViewSet, basename="identifier-type"
)
router.register(r"tags", views.TagViewSet, basename="tag")
router.register(r"authors", views.AuthorViewSet, basename="author")
router.register(r"languages", views.LanguageViewSet, basename="language")

urlpatterns = [
    path("", views.IndexAPIRootView.as_view()),
    path(
        "entries/search/", views.EntrySearchView.as_view(), name="entries-search-list"
    ),
]
urlpatterns += router.urls
