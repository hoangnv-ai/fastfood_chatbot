"""
Router đơn giản: nhận message, phân intent bằng rule-based + keyword,
chuyển cho method_selector để chọn handler và thực thi.
"""
from prompt_engine.method_selector import select_method
from prompt_engine.handlers import (
    zero_shot,
    few_shot,
    chain_of_thought,
    self_ask,
    progressive_summary,
    response_optimizer,
    classify_intent,
)

# mapping tên handler -> function
mapping = {
    "zero_shot": zero_shot.handle_zero_shot,
    "few_shot": few_shot.handle_few_shot,
    "cot": chain_of_thought.handle_cot,
    "self_ask": self_ask.handle_self_ask,
    "progressive_summary": progressive_summary.handle_progressive_summary,
    "optimize": response_optimizer.optimize_response,
}

def route_prompt(user_message: str, context: dict = None):
    """Trả về dict: {"status":..., "response":..., "metadata":...}"""
    context = context or {}

    # phân loại intent__________________________
    intent = classify_intent.handle_intent_classification(user_message).get("intent")
    print(f"Classified intent: {intent}")

    # Chọn hander __________________________
    handler_name = select_method(intent)
    print(f"Intent: {intent}, Handler: {handler_name}")
    handler = mapping.get(handler_name)
    print(f"Using handler function: {handler}")

    # Gọi handler __________________________
    result = handler(user_message, context)

    return {"status":"ok", "response": result.get("text"), "metadata": {"intent": intent, **result.get("meta", {})}}

