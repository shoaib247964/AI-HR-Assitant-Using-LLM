import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

def get_openai_response(message, doc_context=None):
    system_prompt = "You are a helpful AI HR assistant."
    if doc_context:
        system_prompt += "\nReference HR document content below for accurate answers.\n" + doc_context[:3000]  # Limit context for token safety
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
