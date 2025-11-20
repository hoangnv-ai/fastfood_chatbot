from inference.llm_client import call_llm

def handle_progressive_summary(user_message: str, context: dict):
    """
    Progressive summary: dùng khi cuộc hội thoại dài, tóm tắt từng bước.
    """
    history = context.get("history","")
    prompt = f"""
Bạn tóm tắt tiến độ order. History:
{history}
Latest user message:
{user_message}

Hãy trả về summary ngắn gọn (1-2 câu) cập nhật trạng thái đơn hàng.
"""
    reply = call_llm(prompt)
    return {"text": reply, "meta": {"handler":"progressive_summary"}}
