def optimize_response(user_message: str, context: dict):
    """
    Tối ưu response cho phàn nàn / dịch vụ: xác nhận, xin lỗi nếu cần, đề xuất hành động.
    Ở đây dùng template rule-based để tránh gửi private chain-of-thought.
    """
    t = user_message.lower()
    if any(k in t for k in ["bồi thường", "hoàn tiền", "đền bù", "lỗi"]):
        text = ("Xin lỗi về sự bất tiện. Chúng tôi đã ghi nhận vấn đề và sẽ liên hệ sớm nhất. "
                "Vui lòng cung cấp mã đơn hoặc ảnh chụp lỗi để chúng tôi xử lý nhanh hơn.")
    else:
        text = ("Cảm ơn phản hồi của bạn. Chúng tôi rất tiếc về trải nghiệm của bạn. "
                "Nhân viên sẽ liên hệ lại để hỗ trợ chi tiết.")
    return {"text": text, "meta": {"handler":"response_optimizer"}}
