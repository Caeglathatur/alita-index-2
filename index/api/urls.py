from django.urls import path, include

urlpatterns = [
    path('v1/', include('index.api.v1.urls')),
]
