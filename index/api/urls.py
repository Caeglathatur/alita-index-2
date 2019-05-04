from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from django.conf import settings


title = settings.API_DOCS_TITLE if hasattr(
    settings, 'API_DOCS_TITLE') else 'Index REST API Reference'

urlpatterns = [
    path('docs/', include_docs_urls(title=title, permission_classes=[])),
    path('v1/', include('index.api.v1.urls', namespace='v1')),
]
