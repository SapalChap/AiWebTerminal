from openai import OpenAI
from config import OPENROUTER_API_KEY



def get_ai_response(prompt, model = "deepseek"):
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= OPENROUTER_API_KEY
  )

  if model == "deepseek":
    model="deepseek/deepseek-chat-v3.1:free"
  elif model == "llama":
    model="meta-llama/llama-3.3-70b-instruct:free"
  elif model == "gemini":
    model="google/gemini-2.0-flash-exp:free"

  completion = client.chat.completions.create(
    model=model,
    messages=[
      {
        "role": "user",
        "content": prompt
      }
    ]
  )
  return completion.choices[0].message.content
