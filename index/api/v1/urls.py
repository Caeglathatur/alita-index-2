from rest_framework import routers

from .views import EntryViewSet


router = routers.SimpleRouter()
router.register(r'entries', EntryViewSet)

urlpatterns = []
urlpatterns += router.urls
