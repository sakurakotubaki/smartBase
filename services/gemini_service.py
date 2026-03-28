"""
Gemini API連携サービス

将来的にGemini APIを使用して、ナレッジの自動生成を行うためのサービスクラス。
"""

import json
import logging
from dataclasses import dataclass

from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass
class GeneratedContent:
    """Geminiが生成したコンテンツ"""

    title: str
    content: str
    tags: list[str]


class GeminiService:
    """Gemini APIを使用してナレッジを生成するサービス"""

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not set")

    def generate_knowledge(self, raw_input: str) -> GeneratedContent:
        """
        ユーザーの入力からタイトル、本文、タグを生成する

        Args:
            raw_input: ユーザーが入力した元ネタテキスト

        Returns:
            GeneratedContent: 生成されたタイトル、本文、タグ

        Raises:
            NotImplementedError: Gemini API連携が未実装
        """
        # TODO: Gemini APIを使用して実装
        # 期待するプロンプト例:
        # """
        # 以下の入力テキストを元に、ナレッジ記事を作成してください。
        #
        # 入力テキスト:
        # {raw_input}
        #
        # 以下のJSON形式で出力してください:
        # {
        #     "title": "記事のタイトル",
        #     "content": "Markdown形式の本文",
        #     "tags": ["タグ1", "タグ2", "タグ3"]
        # }
        # """
        raise NotImplementedError(
            "Gemini API連携は未実装です。"
            "GEMINI_API_KEYを設定し、このメソッドを実装してください。"
        )

    def _parse_response(self, response_text: str) -> GeneratedContent:
        """
        Gemini APIのレスポンスをパースする

        Args:
            response_text: APIからのレスポンステキスト

        Returns:
            GeneratedContent: パースされたコンテンツ
        """
        try:
            data = json.loads(response_text)
            return GeneratedContent(
                title=data.get("title", ""),
                content=data.get("content", ""),
                tags=data.get("tags", []),
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response: {e}")
            raise ValueError("Gemini APIのレスポンスをパースできませんでした")
