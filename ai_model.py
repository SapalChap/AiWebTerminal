from openai import OpenAI
from config import OPENROUTER_API_KEY


def get_ai_response(prompt):
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= OPENROUTER_API_KEY
  )

  completion = client.chat.completions.create(
    model="deepseek/deepseek-chat-v3.1:free",
    messages=[
      {
        "role": "user",
        "content": prompt
      }
    ]
  )
  return completion.choices[0].message.content
