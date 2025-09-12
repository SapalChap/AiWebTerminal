from openai import OpenAI
from config import OPENROUTER_API_KEY

# Model mapping dictionary - easy to add/modify models
MODEL_MAPPING = {
    "deepseek": "deepseek/deepseek-r1-0528:free",
    "llama": "meta-llama/llama-3.3-70b-instruct:free",
    "gemini": "google/gemini-2.0-flash-exp:free",
    # Add more models here as needed:
    # "gpt4": "openai/gpt-4",
    # "claude": "anthropic/claude-3-sonnet",
}

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
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

def get_available_models():
    """Return list of available model names"""
    return list(MODEL_MAPPING.keys())