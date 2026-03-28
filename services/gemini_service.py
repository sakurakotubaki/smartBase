"""
Gemini API連携サービス

Gemini APIを使用して、ナレッジの自動生成を行うためのサービスクラス。
"""

import json
import logging
import re
from dataclasses import dataclass

from django.conf import settings
from google import genai

logger = logging.getLogger(__name__)


@dataclass
class GeneratedContent:
    """Geminiが生成したコンテンツ"""

    title: str
    content: str
    tags: list[str]


class GeminiService:
    """Gemini APIを使用してナレッジを生成するサービス"""

    SYSTEM_PROMPT = """あなたはナレッジ記事を作成するアシスタントです。
ユーザーの入力テキストを元に、構造化されたナレッジ記事を作成してください。

以下のJSON形式で必ず出力してください（JSONのみを出力、他のテキストは不要）:
{
    "title": "記事のタイトル（簡潔で内容を表すもの）",
    "content": "Markdown形式の本文（見出し、箇条書き、コードブロックなどを適宜使用）",
    "tags": ["タグ1", "タグ2", "タグ3"]
}

注意事項:
- titleは50文字以内で簡潔に
- contentはMarkdown形式で読みやすく構造化
- tagsは3〜5個程度、内容を表すキーワード
- 必ず有効なJSONとして出力すること
"""

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not set")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)

    def generate_knowledge(self, raw_input: str) -> GeneratedContent:
        """
        ユーザーの入力からタイトル、本文、タグを生成する

        Args:
            raw_input: ユーザーが入力した元ネタテキスト

        Returns:
            GeneratedContent: 生成されたタイトル、本文、タグ

        Raises:
            ValueError: API未設定またはレスポンスのパースに失敗
        """
        if not self.client:
            raise ValueError(
                "GEMINI_API_KEYが設定されていません。"
                "環境変数にGEMINI_API_KEYを設定してください。"
            )

        prompt = f"""{self.SYSTEM_PROMPT}

入力テキスト:
{raw_input}
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return self._parse_response(response.text)
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise ValueError(f"Gemini APIでエラーが発生しました: {e}")

    def _parse_response(self, response_text: str) -> GeneratedContent:
        """
        Gemini APIのレスポンスをパースする

        Args:
            response_text: APIからのレスポンステキスト

        Returns:
            GeneratedContent: パースされたコンテンツ
        """
        try:
            # 最初と最後の```json ... ```マーカーのみを除去
            # 内部のコードブロックは保持する
            text = response_text.strip()

            # 先頭の```json または ```を除去
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]

            # 末尾の```を除去
            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            data = json.loads(text)
            return GeneratedContent(
                title=data.get("title", ""),
                content=data.get("content", ""),
                tags=data.get("tags", []),
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response: {e}")
            logger.error(f"Response text: {response_text}")
            raise ValueError("Gemini APIのレスポンスをパースできませんでした")
