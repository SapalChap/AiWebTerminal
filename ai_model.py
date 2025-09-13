from openai import OpenAI

try:
  from config import OPENROUTER_API_KEY
except ImportError:
  import os
  OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Model mapping dictionary - easy to add/modify models
MODEL_MAPPING = {
    "deepseek": "deepseek/deepseek-chat-v3.1:free",
    "llama": "meta-llama/llama-3.3-70b-instruct:free",
    "gemini": "google/gemini-2.0-flash-exp:free",
    # Add more models here as needed:
    # "gpt4": "openai/gpt-4",
    # "claude": "anthropic/claude-3-sonnet",
}




system_prompt = """
-You are a coding assistant called "AI Web Terminal Coding Assistant". 
When you provide code, always enclose it in triple backticks and mark the block with a unique identifier.
The format must be:

```<language> :  code block <n> start
<code>
``` code block <n> end 

Where <n> is a sequential number starting from 1.
- You must always provide code in the format specified above.

- You must always introduce yourself as "AI Web Terminal Coding Assistant"
- You must always explain your reasoning step by step.
-Act like a professional - speak in a professional manner. No emojis.
-Speak in English only. 


-Always start your response with "Start AI Response --- " and end with " --- End AI Response"

"""


def get_ai_response(prompt, model="deepseek"):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY
    )

    # Get the actual model name from the mapping
    actual_model = MODEL_MAPPING.get(model, MODEL_MAPPING["deepseek"])
    
    # If model not found, fallback to deepseek and log it
    if model not in MODEL_MAPPING:
        print(f"Warning: Model '{model}' not found, using deepseek instead")

    completion = client.chat.completions.create(
        model=actual_model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

def get_available_models():
    """Return list of available model names"""
    return list(MODEL_MAPPING.keys())