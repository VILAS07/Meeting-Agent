import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def call_llm(prompt: str, model: str = 'stepfun/step-3.5-flash:free', max_tokens: int = None, stream: bool = True) -> str:
    """
    Calls the OpenRouter API with the given prompt and model.
    Includes streaming support and a fallback to a secondary free model if the first one fails.
    
    Args:
        prompt (str): The prompt space to send to the LLM.
        model (str): The model identifier to use.
        max_tokens (int, optional): Max tokens to generate.
        stream (bool): Whether to stream to console.
        
    Returns:
        str: The full response text from the LLM.
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
        ],
        "stream": stream
    }
    if max_tokens:
        payload["max_tokens"] = max_tokens
        
    def _execute_request(current_payload):
        response = requests.post(url, headers=headers, json=current_payload, stream=stream, timeout=30)
        response.raise_for_status()
        
        full_text = ""
        if stream:
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith("data: "):
                        data_str = line_str[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    chunk = delta['content']
                                    print(chunk, end='', flush=True)
                                    full_text += chunk
                        except json.JSONDecodeError:
                            pass
            print() # Print newline exactly after stream finishes
            return full_text
        else:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                raise ValueError(f"Unexpected response format: {result}")

    try:
        return _execute_request(payload)
    except requests.exceptions.RequestException as e:
        print(f"\nError with primary model {model}: {e}. Retrying with fallback model.")
        
        # Fallback implementation
        fallback_model = 'google/gemma-2-9b-it:free'
        payload["model"] = fallback_model
        
        try:
            return _execute_request(payload)
        except requests.exceptions.HTTPError as fallback_error:
            if fallback_error.response.status_code == 404:
                # If everything 404s, use openai/gpt-3.5-turbo logic or pure string
                print(f"Fallback model 404ed. Trying microsoft/phi-3-mini-128k-instruct:free")
                payload["model"] = 'microsoft/phi-3-mini-128k-instruct:free'
                try:
                    return _execute_request(payload)
                except Exception as e:
                    return "{}"
            return "{}"
        except Exception as e:
            return "{}"
