from django.urls import path
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'entries', views.EntryViewSet, basename='entry')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(
    r'length-units',
    views.LengthUnitViewSet,
    basename='length-unit',
)
router.register(
    r'identifier-types',
    views.IdentifierTypeViewSet,
    basename='identifier-type',
)
router.register(
    r'tags',
    views.TagViewSet,
    basename='tag',
)
router.register(
    r'authors',
    views.AuthorViewSet,
    basename='author',
)

urlpatterns = [
    path('', views.IndexAPIRootView.as_view()),
]
urlpatterns += router.urls
