import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inference.llm_client import call_llm

menu_path = "/Users/admin/Documents/HUST/NentangAItaosinh/fastfood-chatbot/data/menu.json"
with open(menu_path, "r", encoding="utf-8") as f:
    menu_json = f.read()


def handle_zero_shot(user_message: str, context: dict):
    """
    Trường hợp: đặt món đơn giản / hỏi thông tin nhanh.
    Dùng một prompt zero-shot gửi tới LLM.
    """

    prompt = [
        {
                "role": "assistant",
                "content": f"""Bạn là trợ lý bán hàng nhanh Highlands Coffee.Hãy trả lời hoặc nhận đơn đặt hàng từ khách hàng dựa trên các
                                HƯỚNG DẪN:
                                - Luôn dùng dữ liệu trong MENU_JSON bên dưới.
                                - Không tự bịa món.
                                - Trong trường hợp người dùng gọi món, hãy:
                                + Xác nhận số lượng và tên món khách hàng đã gọi. Không đặt câu hỏi ngược lại.
                                + Hỏi thêm khách hàng có muốn gọi thêm món gì trong menu nữa không.  
                                + Trả lời ngắn gọn, lịch sự.

                                Dưới đây là MENU_JSON:
                                {menu_json}
                                Hãy trả lời ngắn gọn và lịch sự.
                                Lịch sử trò chuyện:
                                {context.get("history", "")}
                        """
        },
        {
                "role": "user",
                "content": f"{user_message}"
        }
        ]


    reply = call_llm(prompt)
    return {"text": reply, "meta": {"handler":"zero_shot"}}
