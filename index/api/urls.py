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
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

title = (
    settings.API_DOCS_TITLE
    if hasattr(settings, "API_DOCS_TITLE")
    else "Index REST API Reference"
)

urlpatterns = [
    path("docs/", include_docs_urls(title=title, permission_classes=[])),
    path("v1/", include("index.api.v1.urls", namespace="v1")),
]
