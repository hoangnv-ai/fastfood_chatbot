from inference.llm_client import call_llm

menu_path = "/Users/admin/Documents/HUST/NentangAItaosinh/fastfood-chatbot/data/menu.json"
with open(menu_path, "r", encoding="utf-8") as f:
    menu_json = f.read()

def handle_self_ask(user_message: str, context: dict):
    """
    Self-ask / progressive summary handler:
    - Nếu thiếu thông tin: tự hỏi người dùng các câu cần thiết (confirm size, số lượng, lưu ý)
    - Nếu đủ: tóm tắt order và confirm
    """
    
    # --- PROMPT ĐÃ SỬA ĐỔI THEO STYLE HỘI THOẠI ---
    prompt = [
        {
            "role": "assistant",
            "content": f"""Bạn là trợ lý đặt hàng. Nhiệm vụ của bạn là kiểm tra tính đầy đủ của thông tin đặt hàng dựa trên **MENU_JSON** và **Lịch sử trò chuyện**.
                        
                        **MENU_JSON** (Để tham chiếu tên, loại, và các tùy chọn):
                        {menu_json}

                        **HƯỚNG DẪN XỬ LÝ:**
                        1.  **Phân tích:** Đánh giá yêu cầu của người dùng để xem liệu các thông tin quan trọng như **tên món, kích cỡ (size), số lượng, và địa chỉ giao hàng** đã được xác nhận hay chưa.
                        2.  **Thiếu thông tin:** Nếu thiếu bất kỳ thông tin nào cần thiết để hoàn tất đơn hàng, bạn phải trả về **LIST CÁC CÂU HỎI** để hỏi người dùng.
                        3.  **Đủ thông tin:** Nếu đơn hàng có đủ thông tin, bạn phải trả về **BẢN TÓM TẮT ĐƠN HÀNG** chi tiết và chuẩn chỉnh để người dùng xác nhận lần cuối.
                        
                        **Lịch sử trò chuyện:**
                        {context.get("history", "")}

                        **ĐỊNH DẠNG ĐẦU RA BẮT BUỘC (CHỈ DÙNG 1 TRONG 2):**
                        
                        QUESTIONS:
                        - [Câu hỏi 1 cần hỏi người dùng, ví dụ: "Bạn muốn size lớn hay size nhỏ?"]
                        - [Câu hỏi 2 cần hỏi người dùng, ví dụ: "Bạn muốn mấy ly?"]

                        HOẶC

                        SUMMARY:
                        - [Tóm tắt chi tiết 1: Tên món (Size) x Số lượng]
                        - [Tóm tắt chi tiết 2: Tên món (Size) x Số lượng]
                        - [Tổng tiền tạm tính]
                        - [Địa chỉ giao hàng]
                        """
        },
        {
            "role": "user",
            "content": f"Yêu cầu hiện tại của người dùng: \"{user_message}\""
        }
    ]
    # --------------------------------------------------
    
    reply = call_llm(prompt)
    return {"text": reply, "meta": {"handler":"self_ask"}}