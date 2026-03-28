from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """タグモデル"""

    name = models.CharField("タグ名", max_length=50, unique=True)

    class Meta:
        verbose_name = "タグ"
        verbose_name_plural = "タグ"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Knowledge(models.Model):
    """ナレッジモデル"""

    title = models.CharField("タイトル", max_length=200, blank=True)
    raw_input = models.TextField("入力テキスト", help_text="ユーザーが入力する元ネタ")
    content = models.TextField(
        "本文", blank=True, help_text="Geminiが生成するMarkdown形式の本文"
    )
    tags = models.ManyToManyField(Tag, verbose_name="タグ", blank=True, related_name="knowledge_items")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="作成者",
        related_name="knowledge_items",
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "ナレッジ"
        verbose_name_plural = "ナレッジ"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"ナレッジ #{self.pk}"
