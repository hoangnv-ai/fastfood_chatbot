from inference.llm_client import call_llm

menu_path = "/Users/admin/Documents/HUST/NentangAItaosinh/fastfood-chatbot/data/menu.json"
with open(menu_path, "r", encoding="utf-8") as f:
    menu_json = f.read()

def handle_cot(user_message: str, context: dict):
    """
    Handler dùng 'chain-of-thought' style: không cần reveal internal chain-of-thought;
    ta gửi prompt để LLM tính toán từng bước và trả về kết luận.
    Ở production, có thể thay bằng step-by-step deterministic logic (recommended).
    """
    
    # --- PROMPT ĐÃ SỬA ĐỔI THEO STYLE HỘI THOẠI VÀ YÊU CẦU JSON ---
    prompt = [
        {
            "role": "assistant",
            "content": f"""Bạn là một **Trợ lý Tính toán Đơn hàng** chuyên nghiệp Và luôn dùng dữ liệu trong MENU_JSON này {menu_json}. Nhiệm vụ của bạn là phân tích yêu cầu của người dùng dựa trên Lịch sử trò chuyện và thực hiện các bước tính toán sau:
                        **CÁC BƯỚC TÍNH TOÁN BẮT BUỘC (Chain-of-Thought):**
                        1.  **Phân tích Yêu cầu:** Xác định rõ ràng các món hàng, số lượng và giá đơn vị từ yêu cầu.
                        2.  **Tính Tổng Phụ (Subtotal):** Tính tổng tiền của tất cả các món hàng trước khi áp dụng thuế hoặc giảm giá.
                        3.  **Áp dụng Khuyến mãi/Giảm giá (Discount):** Xác định và tính toán chiết khấu/khuyến mãi (nếu có, nếu không thì là 0).
                        4.  **Tính Tổng Thanh toán (Total):** Tính tổng cuối cùng (Subtotal - Discount).

                        **Lịch sử trò chuyện:**
                        {context.get("history", "")}

                        **ĐỊNH DẠNG ĐẦU RA BẮT BUỘC:**
                        Bạn phải trả về kết quả cuối cùng dưới dạng một đối tượng JSON **duy nhất** (không kèm theo bất kỳ lời nói hay giải thích nào khác).

                        {{
                          "items": [
                            {{"name": "Tên món hàng", "quantity": 0, "unit_price": 0, "line_total": 0}},
                            ...
                          ],
                          "subtotal": 0,
                          "discount": 0,
                          "total": 0,
                          "note": "Các ghi chú đặc biệt về đơn hàng hoặc khuyến mãi áp dụng (nếu có)."
                        }}
                        """
        },
        {
            "role": "user",
            "content": f"{user_message}"
        }
    ]
    # ------------------------------------------------------------------
    
    reply = call_llm(prompt)
    return {"text": reply, "meta": {"handler":"cot"}}