from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Knowledge, Tag
from .serializers import KnowledgeCreateSerializer, KnowledgeSerializer, TagSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verify_gemini_api_key(request):
    """Gemini APIキーの検証"""
    api_key = settings.GEMINI_API_KEY

    if not api_key:
        return Response(
            {"status": "error", "message": "GEMINI_API_KEY is not configured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        # モデル一覧を取得してAPIキーの有効性を確認
        models = list(client.models.list())
        model_names = [m.name for m in models[:5]]

        return Response(
            {
                "status": "success",
                "message": "Gemini API key is valid",
                "available_models": model_names,
            }
        )
    except Exception as e:
        return Response(
            {"status": "error", "message": f"API key validation failed: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


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
