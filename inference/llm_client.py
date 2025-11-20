from ollama import chat
from ollama import ChatResponse

def call_llm(prompt: str):
    # print(f"Calling LLM with prompt: {prompt}")
    response: ChatResponse = chat(model='gemma3:1b', 
                                  messages=prompt)
    return response.message.content
