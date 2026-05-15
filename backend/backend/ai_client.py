import anthropic
from django.conf import settings
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



llm = ChatAnthropic(
    model=settings.MINIMAX_MODEL,
    anthropic_api_key=settings.MINIMAX_API_KEY,
    base_url=settings.MINIMAX_BASE_URL,
    max_tokens=1024,
    temperature=0.7)



def chat_with_ai_stream(message: str, history: list = None):
    system_msg = ("system", "你叫小抠脚, 是codejourney.cn网站的AI智能助手, 为用户解决本网站的相关问题。")
    messages = [system_msg]

    # 添加历史消息
    if history:
        for h in history:
            if h.get('role') == 'user':
                messages.append(("human", h.get('content', '')))
            elif h.get('role') == 'assistant':
                messages.append(("ai", h.get('content', '')))

    messages.append(("human", message))
    print(messages)
    prompt = ChatPromptTemplate.from_messages(messages)
    parser = StrOutputParser()
    chain = prompt | llm | parser

    for chunk in chain.stream({"message": message}):
        yield chunk




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
