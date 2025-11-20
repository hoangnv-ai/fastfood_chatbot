"""
Map intent -> handler key used by router.
Bạn có thể thay thế bằng model classifier hoặc rules phức tạp hơn.
"""
def select_method(intent: str) -> str:
    if intent == "simple_order":
        return "zero_shot"
    
    if intent == "multiple_items" or intent == "special_request":
        return "self_ask"
    if intent == "upsell":
        return "few_shot"
    
    if intent == "calc_order":
        return "cot"    
    
    if intent == "complaint":
        return "optimize"
    # default
    return "zero_shot"
