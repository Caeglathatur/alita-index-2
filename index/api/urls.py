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

from django.conf import settings
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


title = (
    settings.INDEX_API_DOCS_TITLE
    if hasattr(settings, "INDEX_API_DOCS_TITLE")
    else "Index REST API Reference"
)

urlpatterns = [
    path(
        "openapi",
        get_schema_view(
            title="Alita Index API Docs",
            # description="API for all things …",
            # version="",
        ),
        name="openapi-schema",
    ),
    path(
        "docs/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="index-api-docs",
    ),
    path("v1/", include("index.api.v1.urls", namespace="v1")),
]
