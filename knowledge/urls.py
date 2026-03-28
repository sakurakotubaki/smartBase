from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import KnowledgeViewSet, TagViewSet

router = DefaultRouter()
router.register("knowledge", KnowledgeViewSet, basename="knowledge")
router.register("tags", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
]
