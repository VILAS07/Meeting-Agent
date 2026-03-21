import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def call_llm(prompt: str, model: str = 'meta-llama/llama-3.1-8b-instruct:free') -> str:
    """
    Calls the OpenRouter API with the given prompt and model.
    Includes a fallback to a secondary free model if the first one fails.
    
    Args:
        prompt (str): The prompt space to send to the LLM.
        model (str): The model identifier to use.
        
    Returns:
        str: The response text from the LLM.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is not set in the .env file.")
        
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/meeting-agent", # Required by OpenRouter for free models
        "X-Title": "Meeting Agent" # Optional, shows in OpenRouter ranking
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            raise ValueError(f"Unexpected response format: {result}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error with primary model {model}: {e}. Retrying with fallback model.")
        
        # Fallback implementation
        fallback_model = 'google/gemma-3-12b-it:free'
        payload["model"] = fallback_model
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                raise ValueError(f"Unexpected response format from fallback: {result}")
                
        except Exception as fallback_error:
            print(f"Fallback model failed: {fallback_error}")
            return "{}" # Return empty JSON so parsing doesn't completely break
