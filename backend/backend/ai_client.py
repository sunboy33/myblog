import anthropic
from django.conf import settings


def generate_article_abstract(text: str) -> str:
    """使用 AI 生成文章摘要"""
    try:
        client = anthropic.Anthropic(
            api_key=settings.MINIMAX_API_KEY,
            base_url=settings.MINIMAX_BASE_URL,
        )

        message = client.messages.create(
            model=settings.MINIMAX_MODEL,
            max_tokens=300,
            system="你是一个文章摘要生成助手。请为用户提供简短准确的摘要，不超过200字，直接返回摘要内容，不要其他解释。",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"请为以下文章生成一段简短的摘要（不超过200字），直接返回摘要内容，不要其他解释：\n\n{text}"
                        }
                    ]
                }
            ]
        )

        for block in message.content:
            if block.type == "text":
                return block.text.strip()
        return ""
    except Exception as e:
        print(f"AI 生成摘要失败: {e}")
        return ""
