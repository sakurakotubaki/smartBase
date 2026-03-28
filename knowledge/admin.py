from django.contrib import admin

from .models import Knowledge, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Knowledge)
class KnowledgeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at", "updated_at")
    list_filter = ("author", "tags", "created_at")
    search_fields = ("title", "raw_input", "content")
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "author")}),
        ("コンテンツ", {"fields": ("raw_input", "content")}),
        ("メタ情報", {"fields": ("tags", "created_at", "updated_at")}),
    )
