from rest_framework import serializers

from .models import Knowledge, Tag


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
    """新規作成用シリアライザ（raw_inputのみ受け取る）"""

    class Meta:
        model = Knowledge
        fields = ["id", "raw_input"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
