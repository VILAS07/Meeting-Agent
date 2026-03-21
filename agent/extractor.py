import json
import os
from .llm import call_llm

def extract_items(transcript: str) -> dict:
    """
    Extracts action items, decisions, people, and topics from a meeting transcript.
    
    Args:
        transcript (str): The raw meeting transcript text.
        
    Returns:
        dict: A dictionary containing the extracted data as parsed from JSON.
              Keys: action_items, decisions, people_mentioned, topics.
    """
    # Load the prompt
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'extract.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
        
    # Inject transcript
    prompt = prompt_template.replace('{transcript}', transcript)
    
    # Call the LLM
    print("Extracting items from transcript...")
    response_text = call_llm(prompt, model='stepfun/step-3.5-flash:free')
    
    # Extract JSON object safely
    start_idx = response_text.find('{')
    end_idx = response_text.rfind('}')
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        response_text = response_text[start_idx:end_idx+1]
        
    response_text = response_text.strip()
    
    # Parse as JSON
    try:
        data = json.loads(response_text)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from extractor: {e}")
        print(f"Raw response: {response_text}")
        return {
            "action_items": [],
            "decisions": [],
            "people_mentioned": [],
            "topics": []
        }
