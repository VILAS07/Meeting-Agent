import json
import os
from .llm import call_llm

def prioritize_items(extracted: dict) -> list:
    """
    Takes extracted items, particularly action_items, and scores them by impact and effort.
    
    Args:
        extracted (dict): Dictionary from extract_items output.
        
    Returns:
        list: List of prioritized items, sorted by highest priority_score.
    """
    action_items = extracted.get("action_items", [])
    if not action_items:
        return []
        
    # Load the prompt
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'prioritize.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
        
    # Inject tasks
    tasks_json_str = json.dumps(action_items, indent=2)
    prompt = prompt_template.replace('{tasks}', tasks_json_str)
    
    # Call the LLM
    print("Prioritizing tasks...")
    response_text = call_llm(prompt)
    
    # Clean response block if it's wrapped in Markdown code blocks
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
        
    response_text = response_text.strip()
    
    # Parse as JSON
    try:
        prioritized = json.loads(response_text)
        # Sort by priority_score descending
        prioritized.sort(key=lambda x: x.get('priority_score', 0), reverse=True)
        return prioritized
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from prioritizer: {e}")
        print(f"Raw response: {response_text}")
        return []
