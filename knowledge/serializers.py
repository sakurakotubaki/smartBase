import logging

from rest_framework import serializers

from services.gemini_service import GeminiService
from .models import Knowledge, Tag

logger = logging.getLogger(__name__)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class KnowledgeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Knowledge
        fields = [
            "id",
            "title",
            "raw_input",
            "content",
            "tags",
            "author",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "title", "content", "tags", "author", "created_at", "updated_at"]


class KnowledgeCreateSerializer(serializers.ModelSerializer):
    """新規作成用シリアライザ（raw_inputのみ受け取る、Geminiで自動生成）"""

    class Meta:
        model = Knowledge
        fields = ["id", "raw_input", "title", "content", "tags"]
        read_only_fields = ["id", "title", "content", "tags"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        raw_input = validated_data.get("raw_input", "")

        # Gemini APIでコンテンツを生成
        try:
            gemini = GeminiService()
            generated = gemini.generate_knowledge(raw_input)

            validated_data["title"] = generated.title
            validated_data["content"] = generated.content

            # ナレッジを作成
            knowledge = Knowledge.objects.create(
                author=validated_data["author"],
                title=validated_data["title"],
                raw_input=raw_input,
                content=validated_data["content"],
            )

            # タグを作成・関連付け
            for tag_name in generated.tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                knowledge.tags.add(tag)

            return knowledge

        except ValueError as e:
            logger.error(f"Gemini generation failed: {e}")
            # Gemini失敗時はraw_inputのみで作成
            return Knowledge.objects.create(
                author=validated_data["author"],
                title="",
                raw_input=raw_input,
                content="",
            )

    def to_representation(self, instance):
        """作成後のレスポンスは詳細シリアライザを使用"""
        return KnowledgeSerializer(instance, context=self.context).data
