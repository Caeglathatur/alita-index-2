from django.urls import path
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'entries', views.EntryViewSet, basename='entry')
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', views.IndexAPIRootView.as_view()),
]
urlpatterns += router.urls
