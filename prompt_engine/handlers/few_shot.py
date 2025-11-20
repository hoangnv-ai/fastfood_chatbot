import json
from multiprocessing import context
from pathlib import Path
from inference.llm_client import call_llm

def load_examples():
    file_path = "/Users/admin/Documents/HUST/NentangAItaosinh/fastfood-chatbot/data/past_orders.json"
    with open(file_path, 'r', encoding='utf-8') as file:
            # Sử dụng json.load() để đọc nội dung tệp và chuyển nó thành dictionary
            examples = json.load(file)
    return examples

menu_path = "/Users/admin/Documents/HUST/NentangAItaosinh/fastfood-chatbot/data/menu.json"
with open(menu_path, "r", encoding="utf-8") as f:
    menu_json = f.read()

def handle_few_shot(user_message: str, context: dict):
    """
    Few-shot: đưa vào ví dụ past_orders để LLM hiểu format upsell / combo.
    """
    examples = load_examples()

    # build few-shot prompt with up to 3 examples
    seed = ""
    for ex in examples[:3]:
        seed += f'''user: {ex.get('user')}
                    assistant: {ex.get('assistant')}\n\n'''

    print("-"*50)
    print("seed :", seed)
    print("-"*50)

    prompt = [
    {
            "role": "assistant",
            "content": f"""Bạn là trợ lý bán hàng nhanh Highlands Coffee.Hãy trả lời hoặc nhận đơn đặt hàng từ khách hàng dựa trên các
                            HƯỚNG DẪN:
                            - Luôn dùng dữ liệu trong MENU_JSON bên dưới.
                            - Không tự bịa món.
                            - Khi người dùng gọi món, hãy:
                            + Chuẩn hóa tên món và size
                            + Tính tổng tiền theo giá trong MENU_JSON
                            + Xuất kết quả dạng rõ ràng
                            - Nếu giá hoặc size không hợp lệ → yêu cầu sửa lại.
                            - Nếu cần đề xuất → ưu tiên món phổ biến hoặc phù hợp giá.

                            Dưới đây là MENU_JSON:
                            {menu_json}
                            Hãy trả lời ngắn gọn và lịch sự.
                            Lịch sử trò chuyện:
                            {context.get("history", "")}

                            Dựa theo ví dụ dưới đây, phản hồi lời đề nghị upsell / combo.
                            {seed}
                    """
    },
    {
            "role": "user",
            "content": f"{user_message}"
    }
    ]
    
    reply = call_llm(prompt)
    return {"text": reply, "meta": {"handler":"few_shot"}}
