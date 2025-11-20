import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inference.llm_client import call_llm

menu_path = "/Users/admin/Documents/HUST/NentangAItaosinh/fastfood-chatbot/data/menu.json"
with open(menu_path, "r", encoding="utf-8") as f:
    menu_json = f.read()

def handle_intent_classification(user_message: str):
    prompt = [
        {
            "role": "assistant",
            "content": """
            Bạn là module *Intent Classifier* cho hệ thống chatbot bán hàng fastfood.

            NHIỆM VỤ:
            - Phân loại câu người dùng vào đúng 1 trong các intent sau:
                1. simple_order        → Đặt 1 món đơn giản, không nhiều yêu cầu.
                2. multiple_items      → Đặt nhiều món hoặc danh sách món.
                3. special_request     → Đặt món có yêu cầu đặc biệt (không đường, không đá, ít ngọt...).
                4. upsell              → Hỏi về combo, khuyến mãi, ưu đãi, upsell.
                5. calc_order          → Hỏi tính tổng tiền, giảm giá, voucher, khuyến mãi.
                6. complaint           → Phản ánh, khiếu nại, phàn nàn, chê dịch vụ.
                7. info                → Hỏi thông tin chung, không thuộc nhóm trên.

            YÊU CẦU TRẢ LỜI:
            - Chỉ trả về **tên intent** thuộc 1 trong 7 intent bên trên không thêm mô tả.
            - Dựa vào nội dung thực tế của người dùng (không phỏng đoán).
            - Nếu không chắc chắn → trả về "info".

            Ví dụ format output hợp lệ:
            simple_order
            multiple_items
            special_request
            upsell
            calc_order
            complaint
            info

            VÍ DỤ:
            User: cho tôi 1 ly trà đào
            → simple_order

            User: cho tôi trà đào và thêm 1 bánh mì chà bông
            → multiple_items

            User: cho ly sữa đá ít đường, không đá
            → special_request

            User: có combo nào rẻ không?
            → upsell

            User: tính tổng giùm tôi 2 ly latte size L
            → calc_order

            User: shipper giao chậm quá
            → complaint

            User: quán mở cửa đến mấy giờ?
            → simple_order   
            
            """
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    reply = call_llm(prompt)
    return {"intent": reply, "meta": {"handler": "intent_classifier"}}
