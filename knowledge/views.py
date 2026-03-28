from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Knowledge, Tag
from .serializers import KnowledgeCreateSerializer, KnowledgeSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """タグの一覧・詳細取得"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class KnowledgeViewSet(viewsets.ModelViewSet):
    """ナレッジのCRUD操作"""

    queryset = Knowledge.objects.select_related("author").prefetch_related("tags")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return KnowledgeCreateSerializer
        return KnowledgeSerializer

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)
