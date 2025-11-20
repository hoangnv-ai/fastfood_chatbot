"""
CLI demo: chạy vòng lặp, nhận message, gọi router và lưu log.
"""
print("Hello world")
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from prompt_engine.prompt_router import route_prompt
from storage.db_manager import init_db, save_log, save_order
import json

def run():
    print("=== FastFood Chatbot demo ===")
    init_db()
    context = {"history": ""}

    while True:
        print("-"*100)
        try:
            user = input("User: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        if not user:
            continue
        save_log("inbound", {"text": user})
        res = route_prompt(user, context)
        
        print("Bot:", res.get("response"))
        save_log("outbound", {"text": res.get("response"), "meta": res.get("metadata")})
        # nếu handler trả về order json (cot), cố lưu
        meta = res.get("metadata", {})
        if meta.get("intent") == "calc_order" and res.get("status") == "ok":
            # cố parse json từ response text (nếu LLM trả JSON)
            try:
                order_obj = json.loads(res.get("response"))
                oid = save_order(order_obj)
                print(f"[Đã lưu order id={oid}]")
            except Exception:
                pass
        # append to history
        context["history"] += f"User: {user}\nBot: {res.get('response')}\n"

if __name__ == "__main__":
    run()
